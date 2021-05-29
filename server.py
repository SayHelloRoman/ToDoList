from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

from orm import Task


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/create_task", response_class=HTMLResponse)
def create_task_get(request: Request):
    return templates.TemplateResponse("create_task.html", {"request": request})


@app.post("/create_task", response_class=RedirectResponse)
async def create_task_post(title_input: str = Form(...), description: str = Form(...)):
    await Task.create(title=title_input, description=description)
    return RedirectResponse(url='/tasks')


@app.get("/tasks", response_class=HTMLResponse)
@app.post("/tasks", response_class=HTMLResponse)
async def create_task_get(request: Request):
    return templates.TemplateResponse("tasks.html", {"request": request, "tasks": await Task.filter().all()})


@app.post("/delete/{id}", response_class=RedirectResponse)
async def create_task_get(request: Request, id: int):
    await Task.filter(id=id).delete()
    return RedirectResponse(url='/tasks')


register_tortoise(
    app,
    db_url="sqlite://:memory:",
    modules={"models": ["orm"]},
    generate_schemas=True,
    add_exception_handlers=True,
)