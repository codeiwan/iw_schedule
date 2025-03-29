import json
from typing import Annotated

from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pathlib import Path

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# 데이터베이스 경로 설정
DB_PATH = Path("database/users.json")

# 로그인 요청 데이터 모델
class LoginRequest(BaseModel):
    username: str
    password: str

# 로그인 페이지 렌더링 (GET 요청)
@router.get("/login")
def login(request: Request):
    username = request.session.get("username")
    if username:
        return RedirectResponse(url="/schedule", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request})

# 로그인 처리 (POST 요청)
@router.post("/login")
def login(request: Request, login_request: Annotated[LoginRequest, Form()]):
    # users.json 파일 읽기
    with open(DB_PATH, "r", encoding="utf-8") as file:
        users = json.load(file)
    
    # 아이디 검증 로직
    for user in users:
        if user["username"] == login_request.username and user["password"] == login_request.password:
            # 로그인 성공 시 세션에 사용자 정보 저장
            request.session["username"] = login_request.username
            return RedirectResponse(url='/schedule', status_code=303)

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "message": "아이디 또는 비밀번호가 잘못되었습니다.",
            "username": login_request.username  # 로그인 시 입력된 아이디를 유지
        }
    )

# 로그아웃 처리 (POST 요청)
@router.post("/logout")
def logout(request: Request):
    # 세션에서 사용자 정보 삭제
    if "username" in request.session:
        del request.session["username"]
    # 로그아웃 후 로그인 페이지로 리다이렉트
    return RedirectResponse(url="/login", status_code=303)
