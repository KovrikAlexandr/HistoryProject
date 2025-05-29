import psycopg2
import os


conn = psycopg2.connect(
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

# conn = psycopg2.connect(
#     database="hist_db",
#     user="admin",
#     password="root",
#     host="localhost",
#     port="13000"
# )


def get_all_epics():
    with conn.cursor() as cur:
        cur.execute("SELECT epic_id, title, description FROM epics ORDER BY title")
        return [{"epic_id": row[0], "title": row[1], "description": row[2]} for row in cur.fetchall()]


def get_epic_by_id(epic_id: str):
    with conn.cursor() as cur:
        cur.execute("SELECT epic_id, title, description FROM epics WHERE epic_id = %s", (epic_id,))
        row = cur.fetchone()
        if row:
            return {"epic_id": row[0], "title": row[1], "description": row[2]}
        return None


def get_events_of_epic(epic_id: str):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT event_date, text FROM events WHERE epic_id = %s ORDER BY event_date ASC",
            (epic_id,)
        )
        return [
            {"date": row[0], "text": row[1]}
            for row in cur.fetchall()
        ]


def get_dependencies_of_epic(epic_id: str):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT depends_on_epic_id FROM epic_dependencies WHERE epic_id = %s",
            (epic_id,)
        )
        return [row[0] for row in cur.fetchall()]


def insert_epic(epic_id: str, title: str, description: str):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO epics (epic_id, title, description) VALUES (%s, %s, %s)",
            (epic_id, title, description)
        )
    conn.commit()


def insert_event(epic_id: str, event_date, text: str):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO events (epic_id, event_date, text) VALUES (%s, %s, %s)",
            (epic_id, event_date, text)
        )
    conn.commit()


def insert_dependency(epic_id: str, depends_on: str):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO epic_dependencies (epic_id, depends_on_epic_id) VALUES (%s, %s)",
            (epic_id, depends_on)
        )
    conn.commit()


def delete_epic_by_id(epic_id: str):
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM epics WHERE epic_id = %s", (epic_id,)
        )
    conn.commit()
    return cur.rowcount > 0


def delete_event_by_id(event_id: int):
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM events WHERE event_id = %s", (event_id,)
        )
    conn.commit()
    return cur.rowcount > 0


def delete_dependency(epic_id: str, depends_on_epic_id: str):
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM dependencies WHERE epic_id = %s AND depends_on_epic_id = %s", (epic_id, depends_on_epic_id)
        )
    conn.commit()
    return cur.rowcount > 0