CREATE TABLE IF NOT EXISTS epics (
    epic_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS epic_dependencies (
    epic_id TEXT REFERENCES epics(epic_id),
    depends_on_epic_id TEXT REFERENCES epics(epic_id) ON DELETE RESTRICT,
    PRIMARY KEY (epic_id, depends_on_epic_id)
);

CREATE TABLE IF NOT EXISTS events (
    event_id SERIAL PRIMARY KEY,
    epic_id TEXT REFERENCES epics(epic_id) NOT NULL,
    event_date DATE NOT NULL,
    text TEXT NOT NULL
);
