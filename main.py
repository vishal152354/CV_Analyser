
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import subprocess
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel 
app = FastAPI()
templates = Jinja2Templates(directory="templates")  #  Specify your templates directory


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)
class Item(BaseModel):
    name: str
    description: str | None = None

@app.get("/getmethod")
async def read_root():
    return {"message": "Hello from FastAPI!"}

# @app.get("/", response_class=HTMLResponse)
# async def read_root(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})


@app.post("/run-python-script",methods=['POST'])
async def run_script():
    print("inside run_script")
    try:
        result = subprocess.run(["python", "view.py", "1"], capture_output=True, text=True, check=True)
        return {"message": f"Python script executed successfully! Output: {result.stdout}"}
    except subprocess.CalledProcessError as e:
        return {"message": f"Error running Python script: {e.stderr}"}