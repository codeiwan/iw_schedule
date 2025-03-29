import json

from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from routes import login, signup, schedule, recorder  # 추가된 라우트 파일
from pathlib import Path

app = FastAPI()

# 세션 미들웨어 추가
app.add_middleware(SessionMiddleware, secret_key="very-secret-key")

# Jinja2 템플릿 연결
templates = Jinja2Templates(directory="templates")

# static 파일을 '/static' 경로로 서빙
app.mount("/static", StaticFiles(directory="static"), name="static")

# 데이터베이스 경로 설정
DB_PATH = Path("database/users.json")

# 서버 시작 시 파일 체크 및 생성
@app.on_event("startup")
def startup_event():
    # 파일이 존재하지 않으면 빈 배열로 작성
    if not DB_PATH.exists():
        with open(DB_PATH, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4, ensure_ascii=False)

# index.html 렌더링
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 라우터 등록
app.include_router(login.router)
app.include_router(signup.router)
app.include_router(schedule.router)
app.include_router(recorder.router)
