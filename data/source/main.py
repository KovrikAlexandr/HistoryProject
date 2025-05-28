from fastapi import FastAPI, HTTPException
from dto import EpicCreate, EventCreate, DependencyCreate
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
    return data.get_events_of_epic(epic_id)


@app.get("/epics/{epic_id}/depends-on")
def get_dependencies_of_epic(epic_id: str):
    return data.get_dependencies_of_epic(epic_id)


@app.post("/epics")
def post_epics(epic: EpicCreate):
    try:
        data.insert_epic(epic.epic_id, epic.title, epic.description)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/events")
def post_events(event: EventCreate):
    try:
        data.insert_event(event.epic_id, event.event_date, event.order_index, event.text)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/dependencies")
def post_dependencies(dep: DependencyCreate):
    try:
        data.insert_dependency(dep.epic_id, dep.depends_on)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
