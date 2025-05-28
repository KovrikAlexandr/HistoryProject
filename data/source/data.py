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
            "SELECT event_date, order_index, text FROM events WHERE epic_id = %s ORDER BY order_index",
            (epic_id,)
        )
        return [
            {"date": row[0], "order": row[1], "text": row[2]}
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


def insert_event(epic_id: str, event_date, order_index: int, text: str):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO events (epic_id, event_date, order_index, text) VALUES (%s, %s, %s, %s)",
            (epic_id, event_date, order_index, text)
        )
    conn.commit()


def insert_dependency(epic_id: str, depends_on: str):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO epic_dependencies (epic_id, depends_on_epic_id) VALUES (%s, %s)",
            (epic_id, depends_on)
        )
    conn.commit()