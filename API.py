from fastapi import FastAPI, Header, Depends, status, Response, Request, APIRouter, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException

from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import random
import json

from scraping.main import scrape_list
from ai_backend import main

async def not_found_error(request: Request, exc: HTTPException):
    return TEMPLATE.TemplateResponse(
        "error.html",
        {
            "request": request,
        }
    )

exception_handlers = {404: not_found_error}
app = FastAPI(exception_handlers=exception_handlers)

app.mount("/static", StaticFiles(directory="static"), name="static")
BASE_PATH = Path(__file__).resolve().parent
TEMPLATE = Jinja2Templates(directory=str(BASE_PATH / "templates"))

# Infrastructure
# @app.get("/favicon.ico")
# async def get_favicon():
#     return FileResponse("static/assets/favicon.ico")

# index
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return TEMPLATE.TemplateResponse(
        "index.html",
        {
            "request": request,
        }
    )


@app.post("/process_data", response_class=HTMLResponse)
async def index(request: Request):
    body = await request.json()
    filepaths = scrape_list(body['url'], body['configurations'])
    analysis = main(filepaths)
    print('Done')
    return json.dumps(analysis)

