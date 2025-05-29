from fastapi import FastAPI, HTTPException
from dto import EpicCreate, EventCreate, Dependency, EpicPatch, EventPatch
import uvicorn
import data

app = FastAPI()

@app.get("/epics")
def get_all_epics():
    return data.get_all_epics()


@app.get("/epics/{epic_id}")
def get_epic_by_id(epic_id: str):
    result = data.get_epic_by_id(epic_id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Epic not found")


@app.get("/epics/{epic_id}/events")
def get_events_of_epic(epic_id: str):
    try:
        return data.get_events_of_epic(epic_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/epics/{epic_id}/depends-on")
def get_dependencies_of_epic(epic_id: str):
    return data.get_dependencies_of_epic(epic_id)


@app.post("/epics")
def post_epic(epic: EpicCreate):
    try:
        data.insert_epic(epic.epic_id, epic.title, epic.description)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/events")
def post_event(event: EventCreate):
    try:
        data.insert_event(event.epic_id, event.event_date, event.text)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/dependencies")
def post_dependency(dep: Dependency):
    try:
        data.insert_dependency(dep.epic_id, dep.depends_on)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@app.delete("/epics/{epic_id}")
def delete_epic(epic_id: str):
    try:
        data.delete_epic_by_id(epic_id)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/events/{event_id}")
def delete_event(event_id: int):
    try:
        data.delete_event_by_id(event_id)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/dependencies")
def delete_dependency(dep: Dependency):
    try:
        data.delete_dependency(dep.epic_id, dep.depends_on_epic_id)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.patch("/epics/{epic_id}")
def patch_epic(epic_id: str, patch: EpicPatch):
    if not data.patch_epic_by_id(epic_id, patch):
        raise HTTPException(status_code=404, detail="Epic not found or no fields provided")
    return {"status": "updated"}


@app.patch("/events/{event_id}")
def patch_event(event_id: int, patch: EventPatch):
    if not data.patch_event_by_id(event_id, patch):
        raise HTTPException(status_code=404, detail="Event not found or no fields provided")
    return {"status": "updated"}



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
