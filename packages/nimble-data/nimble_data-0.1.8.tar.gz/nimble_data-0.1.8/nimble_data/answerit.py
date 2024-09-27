from dataclasses import dataclass
from enum import Enum
from time import sleep
from httpx import Client
from asyncio import sleep as async_sleep
from time import sleep


class Answerit:
    def __init__(self, client):
        self.headers = client.headers
        self.answerit_url = "https://answerit.webit.live"
        self.client = Client(base_url=self.answerit_url, headers=self.headers,
                                  follow_redirects=True)
    def ask_domain_retreival(self, urls: list[str], questions: list[str], most_relevant=True) -> dict:
        request_body = {
            #"depth": 2, "return_most_relevant_content": most_relevant
            "sources": [{"url": url}
                        for url in urls],
            "questions": questions,
            "depth": 2
        }
        response = self.client.post(url="/pipelines/", json=request_body)
        response.raise_for_status()
        json = response.json()
        return self.wait_for_pipeline_execution_to_finish(pipeline_id=json['pipeline_id'],
                                                          pipeline_execution_id=json['pipeline_execution_id'])

    def followup(self, pipeline_id, request_body: dict) -> str:
        response = self.client.patch(url=f"/pipelines/{pipeline_id}", json=request_body)
        response.raise_for_status()
        return response.json()['pipeline_execution_id']
    def get_pipelines(self) -> list[dict]:
        response = self.client.get(f"/pipelines/")
        response.raise_for_status()
        pipelines = response.json()
        return pipelines
    def get_pipeline(self, pipeline_id: str):
        response = self.client.get(f"/pipelines/{pipeline_id}")
        response.raise_for_status()
        pipeline = response.json()
        return pipeline
    def get_pipeline_execution(self, pipeline_id: str, pipeline_execution_id: str):
        response = self.client.get(f"/pipelines/{pipeline_id}/pipeline-executions/{pipeline_execution_id}")
        response.raise_for_status()
        pipeline_execution = response.json()
        return pipeline_execution

    def wait_for_pipeline_execution_to_finish(self, pipeline_id: str, pipeline_execution_id: str):
        pipeline_execution = self.get_pipeline_execution(pipeline_id, pipeline_execution_id)
        attempt_count = 0
        if pipeline_execution['status'] == Status.FAILED.value:
            raise WorkflowFailed()
        while not pipeline_execution['status'] == Status.COMPLETED.value and attempt_count < 600:
            sleep(1)
            print("Processing")
            pipeline_execution = self.get_pipeline_execution(pipeline_id, pipeline_execution_id)
            if pipeline_execution['status'] == Status.FAILED.value:
                raise WorkflowFailed()
            attempt_count += 1
        if attempt_count == 600:
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