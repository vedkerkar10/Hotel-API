# routers/rooms_crud.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db import get_db, Room as DBRoom
from models import Room, RoomCreate
from routers.auth import get_current_user
from routers.rbac import staff_required

router = APIRouter(tags=["Rooms CRUD"])

@router.post("/rooms/", response_model=Room, dependencies=[Depends(staff_required)])
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    db_room = DBRoom(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

@router.get("/rooms/", response_model=List[Room])
def list_rooms(db: Session = Depends(get_db)):
    rooms = db.query(DBRoom).all()
    return rooms

@router.get("/rooms/{room_id}", response_model=Room)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(DBRoom).filter(DBRoom.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.put("/rooms/{room_id}", response_model=Room, dependencies=[Depends(staff_required)])
def update_room(room_id: int, room: RoomCreate, db: Session = Depends(get_db)):
    db_room = db.query(DBRoom).filter(DBRoom.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    for key, value in room.dict().items():
        setattr(db_room, key, value)
    db.commit()
    db.refresh(db_room)
    return db_room

@router.delete("/rooms/{room_id}", dependencies=[Depends(staff_required)])
def delete_room(room_id: int, db: Session = Depends(get_db)):
    db_room = db.query(DBRoom).filter(DBRoom.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(db_room)
    db.commit()
    return {"ok": True}