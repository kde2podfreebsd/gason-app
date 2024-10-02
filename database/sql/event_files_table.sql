CREATE TABLE IF NOT EXISTS event_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    file_path TEXT NOT NULL,
    FOREIGN KEY(event_id) REFERENCES events(id)
);
