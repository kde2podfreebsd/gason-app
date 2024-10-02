CREATE TABLE IF NOT EXISTS admins (
    chatid INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    qr_code_background TEXT NOT NULL,
    qr_code_type TEXT NOT NULL
);
