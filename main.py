
from fastapi import FastAPI,Request,UploadFile,File,HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import subprocess
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel 
from typing import Annotated
import aiofiles 

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


@app.post('/upload_file')
async def upload_file(file: Annotated[UploadFile, File]):
    print("inside upload file")

    try:
         destination_path = r"C:\Users\50054\Desktop\CV_Analyser\data"
         destination_path = os.path.join(destination_path, file.filename)
         print(destination_path)
         async with aiofiles.open(destination_path, "wb") as out_file:
             content = await file.read()  
             await out_file.write(content)
         print(f"File '{file.filename}' successfully saved to '{destination_path}'")
         return {"message": f"File '{file.filename}' uploaded successfully!", "location": destination_path}
    except Exception as e:
        print(f"ERROR: During file upload for '{file.filename}': {e}")
        raise HTTPException(status_code=500, detail=f"Failed to upload file. Server error: {e}")

    


@app.post("/run_python_script")
async def run_script():
    print("inside run_script")
    try:
        result = subprocess.run(["python", r"C:\Users\50054\Desktop\CV_Analyser\backend\view.py", "1"], capture_output=True, text=True, check=True)
        return {"message": f"Python script executed successfully! Output: {result.stdout}"}
    except subprocess.CalledProcessError as e:
        return {"message": f"Error running Python script: {e.stderr}"}
