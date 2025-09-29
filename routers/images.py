# routers/images.py
import os
from fastapi import UploadFile, File, APIRouter, HTTPException

router = APIRouter(tags=["Images"])

@router.post("/rooms/{room_id}/upload-image")
async def upload_image(room_id: int, file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ('.jpg', '.jpeg', '.png'):
        raise HTTPException(status_code=400, detail="image must be jpg or png")
    
    dest = f"static/images/room_{room_id}{ext}"
    with open(dest, "wb") as f:
        content = await file.read()
        f.write(content)

    return {"url": f"/static/images/room_{room_id}{ext}"}