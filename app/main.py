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
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    project = schemas.ProjectCreate(title=title, notes=notes)
    crud.create_project(db, project)
    return RedirectResponse(url="/", status_code=303)

@app.post("/projects/{project_id}/update")
async def update_project(
    project_id: int,
    title: str = Form(...),
    notes: Optional[str] = Form(None),
    is_completed: bool = Form(False),
    db: Session = Depends(get_db)
):
    project = schemas.ProjectCreate(
        title=title,
        notes=notes,
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
    
    # toggle completion status
    project_update = schemas.ProjectCreate(
        title=project.title,
        notes=project.notes,
        is_completed=not project.is_completed
    )
    crud.update_project(db, project_id, project_update)
    return RedirectResponse(url="/", status_code=303)


# API routes for tasks
@app.post("/tasks/")
async def create_task(
    request: Request,
    name: str = Form(...),
    notes: Optional[str] = Form(None),
    project_id: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    # convert empty string to None for project_id
    project_id = int(project_id) if project_id else None
    # create task
    task = schemas.TaskCreate(name=name, notes=notes, project_id=project_id)
    crud.create_task(db, task)
    return RedirectResponse(url="/", status_code=303)

@app.post("/tasks/{task_id}/update")
async def update_task(
    task_id: int,
    name: str = Form(...),
    notes: Optional[str] = Form(None),
    is_completed: bool = Form(False),
    project_id: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    task = schemas.TaskCreate(
        name=name,
        notes=notes,
        is_completed=is_completed,
        project_id=project_id
    )
    crud.update_task(db, task_id, task)
    return RedirectResponse(url="/", status_code=303)

@app.get("/tasks/{task_id}/delete")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    crud.delete_task(db, task_id)
    return RedirectResponse(url="/", status_code=303)

@app.post("/tasks/{task_id}/toggle")
async def toggle_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # toggle completion status
    task_update = schemas.TaskCreate(
        name=task.name,
        notes=task.notes,
        is_completed=not task.is_completed,
        project_id=task.project_id
    )
    crud.update_task(db, task_id, task_update)
    return RedirectResponse(url="/", status_code=303)


# API endpoints (JSON response)
@app.get("/api/projects/", response_model=list[schemas.Project])
def read_projects(skip: int = 0, limit: int = 100,
                  db: Session = Depends(get_db)):
    projects = crud.get_projects(db, skip=skip, limit=limit)
    return projects

@app.get("/api/tasks/", response_model=list[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks


# allow running of dev server via: python -m app.main
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
