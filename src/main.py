from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.db import Base, engine, get_session_db
from app.models.models import Todo

app = FastAPI()
BASE_DIR = Path(__file__).parent

jinja = Jinja2Templates(directory=BASE_DIR / "templates")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/")
def index(request: Request, session: Annotated[Session, Depends(get_session_db)]):
    todos = session.execute(select(Todo)).scalars()
    return jinja.TemplateResponse(request, "index.html", {"todos": todos})


@app.post("/cadastrar-todo", response_class=RedirectResponse)
async def cadastrar_todo(
    request: Request, session: Annotated[Session, Depends(get_session_db)]
):
    form = await request.form()
    title = form.get("title")
    description = form.get("description")

    todo = Todo(title=title, description=description)

    session.add(todo)
    session.commit()

    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/deletar-task/{id}", response_class=RedirectResponse)
def delete_todo(id: int, session: Annotated[Session, Depends(get_session_db)]):
    todo = session.execute(select(Todo).where(Todo.id == id)).scalar_one_or_none()

    session.delete(todo)
    session.commit()

    return RedirectResponse("/", status.HTTP_303_SEE_OTHER)


Base.metadata.create_all(engine)
