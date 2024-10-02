CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    inst_post_url TEXT NOT NULL,
    tg_post_url TEXT NOT NULL,
    button_text TEXT NOT NULL,
    FOREIGN KEY (admin_chatid) REFERENCES admins(chatid)
);
