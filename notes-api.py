from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import json
from typing import Optional

app = FastAPI() #server :o
class Note(BaseModel): #base pydantic model
    text: str
    name: str
    category: str = "Default" #dflt val

path = Path("notes.json")
if not path.is_file(): path.write_text("[]") #create storage file if not already existent

@app.get("/notes") #get all notes (optionally filter by category)
def get_all_notes(category = "all") -> list[Note]:
    notes_list =  json.loads(path.read_text()) #load existing notes
    if category == "all": return notes_list #check if category is specified
    return [note for note in notes_list if note.get("category") == category]

@app.post("/notes") #add note
def create_note(note: Note):
    notes_list = json.loads(path.read_text()) #load all notes
    if get_note_object(note.name, notes_list): raise HTTPException(status_code=400, detail="Note already exists!") #validity
    notes_list.append(note.model_dump()) #append new note (pydantic model -> dict)
    path.write_text(json.dumps(notes_list)) #save to file
    return note

@app.get("/notes/{note_name}") #get single note by name
def get_note(note_name: str) -> Note:
    notes_list = json.loads(path.read_text()) #laod all notes
    note = get_note_object(note_name, notes_list)
    if not note: raise HTTPException(status_code=404, detail="Note not found") #raise error if none found
    return note

class UpdateNote(BaseModel): #base model for path method
    text: Optional[str] = None
    category: Optional[str] = None
    name: Optional[str] = None

@app.patch("/notes/{note_name}")
def update_note(note_name: str, update: UpdateNote):
    notes_list = json.loads(path.read_text()) #load all notes
    note = get_note_object(note_name, notes_list)
    if not note: raise HTTPException(status_code=404, detail="Note not found") #validity

    update_vals = update.model_dump(exclude_unset=True) #@exclude unset vals
    #rase error if user attempts to update name with an already existing val
    if "name" in update_vals and any(o_note.get("name") == update_vals["name"] and o_note != note for o_note in notes_list):
        raise HTTPException(status_code=400, detail="Note already exists!")
    for key, value in update_vals.items(): #actual update
        note[key] = value #update values
    path.write_text(json.dumps(notes_list)) #save to file
    return note

def get_note_object(name, note_list): #no repeating code yipe
    matches = [note for note in note_list if note.get("name") == name]
    if not matches: return None
    return matches[0]
