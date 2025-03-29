import os
from dotenv import load_dotenv

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from openai import OpenAI
from utils.audio import AudioRecorder
from utils.whisper import speech_to_text
from utils.llm import generate_schedule_response

router = APIRouter()
audio = AudioRecorder()
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 녹음 시작 (POST 요청)
@router.post("/start_record")
def start_record():
    if audio.recording:
        return {"message": "녹음이 이미 진행 중입니다."}
    audio.start_recording()
    return {"message": "녹음을 시작합니다."}

# 녹음 완료 (POST 요청)
@router.post("/stop_record")
def stop_record():
    if not audio.recording:
        return {"message": "현재 진행 중인 녹음이 없습니다."}
    audio.stop_recording()
    return {"message": "녹음을 중지하고 파일을 저장합니다."}

# 녹음 취소 (POST 요청)
@router.post("/cancel_record")
def cancel_record():
    if not audio.recording:
        return {"message": "현재 진행 중인 녹음이 없습니다."}
    audio.cancel_recording()
    return {"message": "녹음을 취소합니다."}

@router.post("/stt")
def stt():
    audio_file_path = os.path.join(os.getcwd(), 'audio.wav')
    text_result = speech_to_text(audio_file_path)
    return JSONResponse(content={"text": text_result}, status_code=200)

@router.post("/llm")
def llm():
    client = OpenAI(api_key=api_key)
    message = "4월 10일에 나랑 대표님의 생일이라 선물을 챙겨야 해."
    schedule_result = generate_schedule_response(client, message)
    return JSONResponse(content={"result": schedule_result}, status_code=200)

@router.post("/stt_llm")
def stt_llm():
    audio_file_path = os.path.join(os.getcwd(), 'audio.wav')
    text_result = speech_to_text(audio_file_path)
    client = OpenAI(api_key=api_key)
    schedule_result = generate_schedule_response(client, text_result)

    print("📢 응답 데이터:", schedule_result) 
    return JSONResponse(content={"result": schedule_result}, status_code=200)
