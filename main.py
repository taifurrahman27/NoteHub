from data.notes import notes

def get_notes():
    return notes


print(get_notes())

def create_note(title, content, author):
    note = {
        "id": len(notes) + 1,
        "title": title,
        "content": content,
        "author": author,
    }

    notes.append(note)
    return note

new_note = create_note(
    "Learn Python Functions",
    "Functions help us organize NoteHub code.",
    "Taifur",
)

print(new_note)
print(notes)

def get_note(note_id):
    for note in notes:
        if note["id"] == note_id:
            return note

    return None

print(get_note(2))
print(get_note(99))

def update_note(note_id, title, content):
    note = get_note(note_id)

    if note:
        note["title"] = title
        note["content"] = content
        return note

    return None

print(update_note(2, "FastAPI Basics", "Learning FastAPI for NoteHub."))
print(update_note(99, "Test", "Test"))

def delete_note(note_id):
    note = get_note(note_id)

    if note:
        notes.remove(note)
        return True

    return False

print(delete_note(3))
print(notes)
