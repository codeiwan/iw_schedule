import json
from typing import Annotated

from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from pathlib import Path

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# 데이터베이스 경로 설정
DB_PATH = Path("database/users.json")

# 회원가입 요청 데이터 모델
class SignupRequest(BaseModel):
    username: str
    password: str

# 회원가입 페이지 렌더링 (GET 요청)
@router.get("/signup")
def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

# 회원가입 처리 (POST 요청)
@router.post("/signup")
def signup(request: Request, signup_request: Annotated[SignupRequest, Form()]):
    # users.json 파일 읽기
    with open(DB_PATH, "r", encoding="utf-8") as file:
        users = json.load(file)
    
    # 이미 존재하는 아이디인지 확인
    for user in users:
        if user["username"] == signup_request.username:
            return templates.TemplateResponse(
                "signup.html",
                {"request": request,
                 "message": "이미 존재하는 아이디입니다.",
                 "username": signup_request.username  # 회원가입 시 입력된 아이디를 유지
                }
            )
    
    # 새로운 유저 추가
    new_user = {"username": signup_request.username, "password": signup_request.password}
    users.append(new_user)

    # 파일에 저장
    with open(DB_PATH, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4, ensure_ascii=False)
    
    # 회원가입 성공 후 로그인 페이지로 리다이렉트
    return RedirectResponse(url="/login", status_code=303)
