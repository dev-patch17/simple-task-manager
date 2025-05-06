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
