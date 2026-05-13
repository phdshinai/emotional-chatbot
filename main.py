import os
import sys
import json
import time
import wave
import threading
import tempfile
import pyaudio
from dotenv import load_dotenv
from PIL import Image
from google import genai

# 드라이버 경로 추가
sys.path.append(os.path.expanduser("~/whisplay-ai-chatbot/whisplay/Driver"))
from WhisPlay import WhisPlayBoard
from faces.expressions import get_expression, blink_animation

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SYSTEM_PROMPT_PATH = os.getenv("SYSTEM_PROMPT_PATH", "./prompts/system_prompt.txt")

client = genai.Client(api_key=GEMINI_API_KEY)

# 시스템 프롬프트 로드
with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# 오디오 설정
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CARD_INDEX = 0

# 전역 상태
is_recording = False
board = None
idle_mode = True


def show_expression(emotion):
    """LCD에 표정 표시"""
    img = get_expression(emotion)
    # PIL Image를 RGB565로 변환해서 전송
    img = img.resize((240, 280))
    pixels = []
    for y in range(280):
        for x in range(240):
            r, g, b = img.getpixel((x, y))
            color = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            pixels.extend([(color >> 8) & 0xFF, color & 0xFF])
    board.set_window(0, 0, 239, 279)
    board._send_data(pixels)


def record_audio():
    """버튼 누르는 동안 녹음"""
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        input_device_index=CARD_INDEX,
        frames_per_buffer=CHUNK
    )
    frames = []
    print("[녹음 중...]")
    while is_recording:
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()

    # WAV 파일로 저장
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    wf = wave.open(tmp.name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return tmp.name


def transcribe(wav_path):
    with open(wav_path, "rb") as f:
        audio_data = f.read()
    import base64
    audio_b64 = base64.b64encode(audio_data).decode()
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            genai.types.Part(text="다음 음성을 한국어로 텍스트로 변환해줘. 텍스트만 출력해."),
            genai.types.Part(
                inline_data=genai.types.Blob(
                    mime_type="audio/wav",
                    data=audio_b64
                )
            )
        ]
    )
    return response.text.strip()


def get_response(user_text):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=user_text,
        config=genai.types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        )
    )
    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    try:
        result = json.loads(text)
    except:
        result = {"emotion": "neutral", "speech": text}
    return result


def speak(text):
    try:
        import base64
        import subprocess
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=text,
            config=genai.types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=genai.types.SpeechConfig(
                    voice_config=genai.types.VoiceConfig(
                        prebuilt_voice_config=genai.types.PrebuiltVoiceConfig(
                            voice_name="Aoede"
                        )
                    )
                )
            )
        )
        audio_data = response.candidates[0].content.parts[0].inline_data.data
        if isinstance(audio_data, str):
            audio_data = base64.b64decode(audio_data)

        # 임시 파일로 저장
        tmp = tempfile.NamedTemporaryFile(suffix=".raw", delete=False)
        tmp.write(audio_data)
        tmp.close()

        # ffmpeg으로 리샘플링 후 aplay로 재생
        subprocess.run([
            "ffmpeg", "-y",
            "-f", "s16le", "-ar", "24000", "-ac", "1",
            "-i", tmp.name,
            "-f", "s16le", "-ar", "44100", "-ac", "1",
            "/tmp/tts_out.raw"
        ], capture_output=True)
        os.unlink(tmp.name)

        subprocess.run([
            "aplay", "-f", "S16_LE", "-r", "44100", "-c", "1",
            "-D", "hw:0,0", "/tmp/tts_out.raw"
        ])
    except Exception as e:
        print(f"TTS 오류: {e}")


def idle_animation():
    """대기 중 깜빡임 애니메이션"""
    while True:
        if idle_mode:
            show_expression("calm")
            time.sleep(3)
            show_expression("blink")
            time.sleep(0.15)
        else:
            time.sleep(0.1)


def on_button_press():
    global is_recording, idle_mode
    print("[버튼 누름]")
    idle_mode = False
    is_recording = True
    show_expression("neutral")
    board.set_rgb(0, 0, 50)


def on_button_release():
    global is_recording, idle_mode
    print("[버튼 뗌]")
    is_recording = False


def main():
    global board, idle_mode, is_recording

    print("=== 감성 챗봇 시작 ===")

    # HAT 초기화
    board = WhisPlayBoard()
    board.set_backlight(100)
    board.on_button_press(on_button_press)
    board.on_button_release(on_button_release)

    # 시작 표정
    show_expression("happy")
    time.sleep(1)
    show_expression("calm")

    # 깜빡임 스레드
    blink_thread = threading.Thread(target=idle_animation, daemon=True)
    blink_thread.start()

    print("버튼을 누르고 말하세요.")

    while True:
        # 버튼 눌릴 때까지 대기
        while not is_recording:
            time.sleep(0.05)

        # 녹음
        wav_path = record_audio()

        # 생각하는 표정
        idle_mode = False
        show_expression("concerned")
        board.set_rgb(50, 50, 0)

        try:
            # 음성인식
            print("[음성인식 중...]")
            user_text = transcribe(wav_path)
            print(f"[인식됨]: {user_text}")
            os.unlink(wav_path)

            # 감성 응답
            print("[응답 생성 중...]")
            result = get_response(user_text)
            emotion = result.get("emotion", "neutral")
            speech = result.get("speech", "")
            print(f"[감정]: {emotion}")
            print(f"[응답]: {speech}")

            # 표정 표시
            show_expression(emotion)
            board.set_rgb(0, 50, 0)

            # 음성 출력
            speak(speech)

        except Exception as e:
            print(f"오류: {e}")
            show_expression("concerned")

        finally:
            # 대기 상태로 복귀
            time.sleep(1)
            idle_mode = True
            board.set_rgb(0, 0, 0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n종료합니다.")
        if board:
            board.cleanup()