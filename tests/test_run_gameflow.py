import uuid, pytest
from temporalio.worker import Worker
from temporalio.testing import WorkflowEnvironment

from quests import accept_bounty, find_target, is_target_alive, capture_target, return_target
from gameflow import CaptureTarget

@pytest.mark.asyncio
async def test_execute_workflow():
    task_queue_name = str(uuid.uuid4())
    async with await WorkflowEnvironment.start_time_skipping() as env:

        async with Worker(
            env.client,
            task_queue=task_queue_name,
            workflows=[CaptureTarget],
            activities=[accept_bounty, find_target, is_target_alive, capture_target, return_target],
        ):
            response = await env.client.execute_workflow(
                CaptureTarget.run,
                "Jimmy Workflow",
                id=str(uuid.uuid4()),
                task_queue=task_queue_name,
            )
        assert isinstance(response, bool), "Response is not a boolean"
        print("***********Workflow Tested Successfully***********")

