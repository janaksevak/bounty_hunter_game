import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from gameflow import CaptureTarget
from quests import accept_bounty, find_target, is_target_alive, capture_target, return_target
from globals import CAPTURE_TARGET_TASK_QUEUE


async def bounty_hunting():
    """
    This function is the main entry point for the script.
    It creates a Temporal client, registers the workflow and activities, and starts the worker.
    """
    # Create a Temporal client
    client = await Client.connect("localhost:7233", namespace="default") #bounty_hunter_namespace

    # Create a worker to process tasks from the "capture-target" task queue
    worker = Worker(
        client=client,
        task_queue=CAPTURE_TARGET_TASK_QUEUE,
        workflows=[CaptureTarget],
        activities=[accept_bounty, find_target, is_target_alive, capture_target, return_target],
    )

    # Start the worker
    await worker.run()
    

if __name__ == "__main__":
    # Run the main function
    asyncio.run(bounty_hunting())
