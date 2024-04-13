from fastapi import FastAPI, File, UploadFile, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from apiConnection import Create_Service, removeAccount
from fastapi.responses import JSONResponse
import uvicorn
import re
import requests
import json
import gdown
from components.ImageList import list_files_in_google_drive_folder
from typing import Dict
import gdown, sys
from checkPath.Get_URL import GET_THE_URL

CLIENT_FILE_NAME = "./client_secret.json"
API_DRIVE = "drive"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/drive"]

services = Create_Service(CLIENT_FILE_NAME, API_DRIVE, API_VERSION, SCOPES)

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/details")
async def get_detail():
    dwn_url = GET_THE_URL()
    # url = "https://drive.google.com/file/d/1ojnzKbvrBJI9NjAbPkefld1Zc1ps4kK_/view?usp=sharing"
    # file_id = url.split("/")[-2]
    # dwn_url = "https://drive.google.com/uc?id=" + file_id
    try:
        response = requests.get(dwn_url)
        # response.raise_for_status()
        json_data = response.json()
        return JSONResponse(
            status_code=200, content={"data": json_data, "success": True}
        )
    except requests.exceptions.RequestException as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to download the file: {e}", "success": False},
        )


@app.delete("/api/logout")
async def delete_account():
    removeAccount()


@app.post("/api/getImages")
async def get_images(req: Dict[str, str]):
    url = req.get("url")
    file_ids = list_files_in_google_drive_folder(url)
    if file_ids:
        return JSONResponse(
            content={
                "message": "Successfully added Report and Summary",
                "data": file_ids,
                "success": True,
            }
        )
    else:
        print("No files found in the folder.")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
