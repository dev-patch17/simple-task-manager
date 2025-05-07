from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional

from . import models, schemas, crud
from .database import engine, get_db

# create database tables
models.Base.metadata.create_all(bind=engine)

# initialize FastAPI
app = FastAPI(title='Simple Task Manager')

# set up templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# index route
@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    projects = crud.get_projects(db)
    tasks = crud.get_tasks(db)
    return templates.TemplateResponse('index.html', {
        'request': request,
        'projects': projects,
        'tasks': tasks
    })


# API routes for projects
@app.post("/projects/")
async def create_project(
    request: Request,
    title: str = Form(...),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    project = schemas.ProjectCreate(title=title, description=description)
    crud.create_project(db, project)
    return RedirectResponse(url="/", status_code=303)

@app.post("/projects/{project_id}/update")
async def update_project(
    project_id: int,
    title: str = Form(...),
    description: Optional[str] = Form(None),
    is_completed: bool = Form(False),
    db: Session = Depends(get_db)
):
    project = schemas.ProjectCreate(
        title=title,
        description=description,
        is_completed=is_completed
    )
    crud.update_project(db, project_id, project)
    return RedirectResponse(url="/", status_code=303)

@app.get("/projects/{project_id}/delete")
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    crud.delete_project(db, project_id)
    return RedirectResponse(url="/", status_code=303)

@app.post("/projects/{project_id}/toggle")
async def toggle_project(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Toggle completion status
    project_update = schemas.ProjectCreate(
        title=project.title,
        description=project.description,
        is_completed=not project.is_completed
    )
    crud.update_project(db, project_id, project_update)
    return RedirectResponse(url="/", status_code=303)
