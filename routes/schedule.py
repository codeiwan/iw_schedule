from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# 스케줄 페이지 렌더링 (GET 요청)
@router.get("/schedule")
def schedule(request: Request):
    username = request.session.get("username")
    if username:
        return templates.TemplateResponse("schedule.html", {"request": request, "username": username})
    return RedirectResponse(url="/login", status_code=303)
