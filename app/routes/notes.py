from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database
from app.auth import get_current_user

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)

# Create a note
@router.post("/", response_model=schemas.NoteOut)
def create_note(note: schemas.NoteCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    new_note = models.Note(title=note.title, content=note.content, owner_id=current_user.id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

# Get all notes for current user
@router.get("/", response_model=List[schemas.NoteOut])
def get_notes(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Note).filter(models.Note.owner_id == current_user.id).all()

# Get a specific note
@router.get("/{note_id}", response_model=schemas.NoteOut)
def get_note(note_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# Update a note
@router.put("/{note_id}", response_model=schemas.NoteOut)
def update_note(note_id: int, updated_note: schemas.NoteCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note.title = updated_note.title
    note.content = updated_note.content
    db.commit()
    db.refresh(note)
    return note

# Delete a note
@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()
    return None
