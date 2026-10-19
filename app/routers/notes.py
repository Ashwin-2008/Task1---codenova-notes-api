from fastapi import APIRouter, HTTPException, status

from app.controllers import note_controller
from app.schemas.note import NoteCreate, NoteResponse, NoteUpdate

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get("", response_model=list[NoteResponse])
def get_all_notes():
    return note_controller.list_notes()


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int):
    note = note_controller.get_note(note_id)

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return note


@router.post(
    "",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_note(data: NoteCreate):
    return note_controller.create_note(data)


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, data: NoteUpdate):
    note = note_controller.update_note(note_id, data)

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return note


@router.delete("/{note_id}", status_code=status.HTTP_200_OK)
def delete_note(note_id: int):
    deleted = note_controller.delete_note(note_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found")

    return {
        "success": True,
        "message": "Note deleted successfully",
    }