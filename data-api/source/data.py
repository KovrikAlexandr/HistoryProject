from typing import Optional

import psycopg2
import os
from dto import EpicPatch, EventPatch


conn = psycopg2.connect(
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)


def get_all_epics():
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT epic_id, title, description FROM epics ORDER BY title")
            return [{"epic_id": row[0], "title": row[1], "description": row[2]} for row in cur.fetchall()]
    except Exception as e:
        conn.rollback()
        raise e


def get_epic_by_id(epic_id: str):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT epic_id, title, description FROM epics WHERE epic_id = %s", (epic_id,))
            row = cur.fetchone()
            if row:
                return {"epic_id": row[0], "title": row[1], "description": row[2]}
            return None
    except Exception as e:
        conn.rollback()
        raise e


def get_events_of_epic(epic_id: str):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT event_id, event_date, text FROM events WHERE epic_id = %s ORDER BY event_date ASC",
                (epic_id,)
            )
            return [
                {"id": row[0], "date": row[1], "text": row[2]}
                for row in cur.fetchall()
            ]
    except Exception as e:
        conn.rollback()
        raise e


def get_dependencies_of_epic(epic_id: str):
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT dep.depends_on_epic_id, e.title, e.description
                FROM epic_dependencies as dep
                    JOIN epics AS e ON dep.depends_on_epic_id = e.epic_id
                WHERE dep.epic_id = %s
                """,
                (epic_id,)
            )
            return [
                {"depends_on_epic_id": row[0], "title": row[1], "description": row[2]}
                for row in cur.fetchall()
            ]
    except Exception as e:
        conn.rollback()
        raise e


def insert_epic(epic_id: str, title: str, description: str):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO epics (epic_id, title, description) VALUES (%s, %s, %s)",
                (epic_id, title, description)
            )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e


def insert_event(epic_id: str, event_date, text: str):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO events (epic_id, event_date, text) VALUES (%s, %s, %s)",
                (epic_id, event_date, text)
            )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e


def insert_dependency(epic_id: str, depends_on: str, description: Optional[str] = None):
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO epic_dependencies (epic_id, depends_on_epic_id, description)
                VALUES (%s, %s, %s)
                """,
                (epic_id, depends_on, description)
            )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e



def delete_epic_by_id(epic_id: str):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM epics WHERE epic_id = %s", (epic_id,)
            )
        if cur.rowcount == 0:
            raise Exception(f"No epic with ID: {epic_id}")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e


def delete_event_by_id(event_id: int):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM events WHERE event_id = %s", (event_id,)
            )
        if cur.rowcount == 0:
            raise Exception(f"No event with ID: {event_id}")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e


def delete_dependency(epic_id: str, depends_on_epic_id: str):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM epic_dependencies WHERE epic_id = %s AND depends_on_epic_id = %s", (epic_id, depends_on_epic_id)
            )
        if cur.rowcount == 0:
            raise Exception(f"No dependency found: {epic_id} doesn't depend on {depends_on_epic_id}")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e


def update_epic(epic_id: str, patch: EpicPatch):
    fields, values = [], []
    if patch.title is not None:
        fields.append("title = %s")
        values.append(patch.title)
    if patch.description is not None:
        fields.append("description = %s")
        values.append(patch.description)
    if not fields:
        return False
    values.append(epic_id)
    try:
        with conn.cursor() as cur:
            cur.execute(f"UPDATE epics SET {', '.join(fields)} WHERE epic_id = %s", tuple(values))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise


def update_event(event_id: int, patch: EventPatch):
    fields, values = [], []
    if patch.epic_id is not None:
        fields.append("epic_id = %s")
        values.append(patch.epic_id)
    if patch.event_date is not None:
        fields.append("event_date = %s")
        values.append(patch.event_date)
    if patch.text is not None:
        fields.append("text = %s")
        values.append(patch.text)
    if not fields:
        return False
    values.append(event_id)
    try:
        with conn.cursor() as cur:
            cur.execute(f"UPDATE events SET {', '.join(fields)} WHERE id = %s", tuple(values))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise


def update_dependency(epic_id: str, depends_on: str, description: str):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE epic_dependencies SET description = %s WHERE epic_id = %s AND depends_on_epic_id = %s",
                (description, epic_id, depends_on)
            )
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise


