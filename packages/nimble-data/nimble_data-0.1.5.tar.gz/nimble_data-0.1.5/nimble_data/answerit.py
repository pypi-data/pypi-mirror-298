from dataclasses import dataclass
from enum import Enum
from time import sleep
from httpx import AsyncClient
from asyncio import sleep as async_sleep
from time import sleep


class Answerit:
    def __init__(self, client):
        self.headers = client.headers
        self.answerit_url = "https://answerit.webit.live"
        self.client = AsyncClient(base_url=self.answerit_url, headers=self.headers,
                                  follow_redirects=True)
    async def create_pipeline(self, request_body: dict) -> dict:
        response = await self.client.post(url="/pipelines/", json=request_body)
        response.raise_for_status()
        return response.json()
    async def update_pipeline(self, pipeline_id, request_body: dict) -> str:
        response = await self.client.patch(url=f"/pipelines/{pipeline_id}", json=request_body)
        response.raise_for_status()
        return response.json()['pipeline_execution_id']
    async def get_pipelines(self) -> list[dict]:
        response = await self.client.get(f"/pipelines/")
        response.raise_for_status()
        pipelines = response.json()
        return pipelines
    async def get_pipeline(self, pipeline_id: str):
        response = await self.client.get(f"/pipelines/{pipeline_id}")
        response.raise_for_status()
        pipeline = response.json()
        return pipeline
    async def get_pipeline_execution(self, pipeline_id: str, pipeline_execution_id: str):
        response = await self.client.get(f"/pipelines/{pipeline_id}/pipeline-executions/{pipeline_execution_id}")
        response.raise_for_status()
        pipeline_execution = response.json()
        return pipeline_execution
    async def wait_for_pipeline_execution_to_finish(self, pipeline_id: str, pipeline_execution_id: str):
        pipeline_execution = await self.get_pipeline_execution(pipeline_id, pipeline_execution_id)
        attempt_count = 0
        if pipeline_execution['status'] == Status.FAILED.value:
            raise WorkflowFailed()
        while not pipeline_execution['status'] == Status.COMPLETED.value and attempt_count < 30:
            await async_sleep(10)
            pipeline_execution = await self.get_pipeline_execution(pipeline_id, pipeline_execution_id)
            if pipeline_execution['status'] == Status.FAILED.value:
                raise WorkflowFailed()
            attempt_count += 1
        if attempt_count == 30:
            raise WorkflowTimeout()
        return pipeline_execution


class Status(Enum):
    PENDING = 'Pending'
    INPROGRESS = 'InProgress'
    COMPLETED = 'Completed'
    FAILED = 'Failed'


class WorkflowFailed(Exception):
    def __init__(self):
        super().__init__()
class WorkflowTimeout(Exception):
    def __init__(self):
        super().__init__()