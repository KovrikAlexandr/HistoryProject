import httpx

class HistDataClient:
    def __init__(self, data_api_url: str):
        self.data_api_url = data_api_url

    async def get_all_epics(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.data_api_url}/epics")
            response.raise_for_status()
            return response.json()


    async def get_epic_data(self, epic_id: str):
        async with httpx.AsyncClient() as client:
            epic_resp = await client.get(f"{self.data_api_url}/epics/{epic_id}")
            epic_resp.raise_for_status()
            epic = epic_resp.json()

            deps_resp = await client.get(f"{self.data_api_url}/epics/{epic_id}/depends-on")
            deps_resp.raise_for_status()
            dependencies = deps_resp.json()

            events_resp = await client.get(f"{self.data_api_url}/epics/{epic_id}/events")
            events_resp.raise_for_status()
            events = events_resp.json()

            return epic["title"], epic["description"], dependencies, events
