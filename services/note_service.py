from data.notes import notes


def get_notes():
    return notes


def create_note(title, content, author):
    note = {
        "id": len(notes) + 1,
        "title": title,
        "content": content,
        "author": author,
    }

    notes.append(note)
    return note


def get_note(note_id):
    for note in notes:
        if note["id"] == note_id:
            return note
    return None


def update_note(note_id, title, content):
    note = get_note(note_id)

    if note:
        note["title"] = title
        note["content"] = content
        return note

    return None


def delete_note(note_id):
    note = get_note(note_id)

    if note:
        notes.remove(note)
        return True

    return False
