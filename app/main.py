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
@app.get('/', response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    projects = crud.get_projects(db)
    tasks = crud.get_tasks(db)
    return templates.TemplateResponse('index.html', {
        'request': request,
        'projects': projects,
        'tasks': tasks
    })
