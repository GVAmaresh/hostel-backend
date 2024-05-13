from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from components.ImageList import list_files_in_google_drive_folder
from typing import Dict


app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        
@app.get("/api/getImformation")
async def get_imf():
        return JSONResponse(
            content={
                "message": "Successfully API Working",
                "data": None,
                "success": True,
            }
        )
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
