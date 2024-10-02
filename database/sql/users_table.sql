CREATE TABLE IF NOT EXISTS users (
    chatid INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    first_name TEXT,
    second_name TEXT,
    phone TEXT,
    qrcode_path TEXT
);
