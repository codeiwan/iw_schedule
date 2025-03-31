import json

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from pathlib import Path
from pydantic import BaseModel

router = APIRouter()
templates = Jinja2Templates(directory="templates")

SCHEDULE_PATH = Path("database/schedules.json")
PRIMEKEY_DB_PATH = Path("database/primekey.json")

"""JSON 파일에서 일정 데이터 불러오기"""
def load_schedules():
    with open(SCHEDULE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

""" 일정 데이터 모델 정의 """
class ScheduleItem(BaseModel):
    username: str
    date: str
    title: str
    content: str

# 스케줄 페이지 렌더링 (GET 요청)
@router.get("/schedule")
def schedule(request: Request):
    username = request.session.get("username")
    if username:
        return templates.TemplateResponse("schedule.html", {"request": request, "username": username})
    return RedirectResponse(url="/login", status_code=303)

# 사용자 디테일 페이지 렌더링 (GET 요청)
@router.get("/schedule/{username}")
def get_schedule(username: str, request: Request):
    if not request.session.get("username") or request.session.get("username") != username:
        return RedirectResponse(url="/schedule", status_code=303)
    schedules = load_schedules()
    user_schedules = [schedule for schedule in schedules if schedule["username"] == username]
    return templates.TemplateResponse("detail.html", {"request": request, "schedules": user_schedules, "username": username})

# 일정 추가
@router.post("/add_schedule")
def add_schedule(schedule: ScheduleItem):
    schedules = load_schedules()

    # PRIMEKEY_DB_PATH에서 schedule_id 값 읽기
    with open(PRIMEKEY_DB_PATH, "r", encoding="utf-8") as file:
        primekey_data = json.load(file)
        
    new_schedule = dict()
    new_schedule["pk"] = primekey_data["schedule"]
    new_schedule.update(schedule.dict())

    schedules.append(new_schedule)

    primekey_data["schedule"] += 1

    # 변경된 schedule_id 값을 다시 파일에 저장
    with open(PRIMEKEY_DB_PATH, "w", encoding="utf-8") as file:
        json.dump(primekey_data, file, indent=4, ensure_ascii=False)

    with open(SCHEDULE_PATH, "w", encoding="utf-8") as file:
        json.dump(schedules, file, ensure_ascii=False, indent=4)

    return JSONResponse(content={"message": "일정이 추가되었습니다!"}, status_code=201)
