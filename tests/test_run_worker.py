import uuid
import pytest
from temporalio import activity
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker
from gameflow import CaptureTarget 

# Mock activities
@activity.defn(name="accept_bounty")
async def mock_accept_bounty(target_name: str) -> bool:
    print(f"***********Mock Bounty for Target {target_name} accepted***********")    
    return True

@activity.defn(name="find_target")
async def mock_find_target(target_name: str) -> bool:
    print(f"***********Mock Found Target {target_name}***********")    
    return True

@activity.defn(name="is_target_alive")
async def mock_is_target_alive(target_name: str) -> bool:
    print(f"***********Mock Target {target_name} is alive***********")    
    return True

@activity.defn(name="capture_target")
async def mock_capture_target(target_name: str) -> bool:
    print(f"***********Mock Captured Target {target_name}***********")    
    return True

@activity.defn(name="return_target")
async def mock_return_target(target_name: str) -> bool:
    print(f"***********Mock Returned Target {target_name}***********")    
    return True

@pytest.mark.asyncio
async def test_mock_activity():
    task_queue_name = str(uuid.uuid4())
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue=task_queue_name,
            workflows=[CaptureTarget],
            activities=[
                mock_accept_bounty,
                mock_find_target,
                mock_is_target_alive,
                mock_capture_target,
                mock_return_target,
            ],
        ):
            response = await env.client.execute_workflow(
                CaptureTarget.run,
                "Jimmy Worker",
                id=str(uuid.uuid4()),
                task_queue=task_queue_name,
            )
            assert isinstance(response, bool), "Response is not a boolean"
            print("***********Worker Tested successfully***********")

