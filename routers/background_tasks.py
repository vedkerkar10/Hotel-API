# routers/background_tasks.py
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session
import time

from db import get_db, Room, Booking
from models import BookingCreate

router = APIRouter(tags=["Background Tasks"])

def send_confirmation_email(booking_id: int, email: str):
    # simulated long-running action
    time.sleep(1)
    print(f"Sent confirmation for booking {booking_id} to {email}")

def create_booking_sync(payload: BookingCreate, db: Session):
    if payload.start_date > payload.end_date:
        raise HTTPException(status_code=400, detail="end_date must be after start_date")

    room = db.query(Room).filter(Room.id == payload.room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="room not found")

    conflict = db.query(Booking).filter(
        Booking.room_id == payload.room_id,
        Booking.start_date < payload.end_date,
        Booking.end_date > payload.start_date
    ).first()

    if conflict:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="room already booked for these dates")

    b = Booking(
        room_id=payload.room_id,
        start_date=payload.start_date,
        end_date=payload.end_date,
        guest_name=payload.guest_name
    )

    db.add(b)
    db.commit()
    db.refresh(b)
    return b

@router.post("/bookings_with_email/")
def book_with_email(payload: BookingCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    booking = create_booking_sync(payload, db)
    
    background_tasks.add_task(send_confirmation_email, booking.id, 
                                 payload.guest_name or "guest@example.com")
    
    return {"booking_id": booking.id, "status": "confirmed (email queued)"}