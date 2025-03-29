import json

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pathlib import Path

router = APIRouter()
templates = Jinja2Templates(directory="templates")

SCHEDULE_PATH = Path("database/schedules.json")

"""JSON 파일에서 일정 데이터 불러오기"""
def load_schedules():
    with open(SCHEDULE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

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
