import asyncio
from temporalio.client import Client
from gameflow import CaptureTarget
from globals import CAPTURE_TARGET_TASK_QUEUE, logger

logger.name = "run_gameflow"

async def execute_workflow(target_name: str):
    """
    This function is the main entry point for the script.
    It creates a Temporal client, registers the workflow and activities, and starts the worker.
    """
    # Create a Temporal client 
    client = await Client.connect("localhost:7233")

    # Register the workflow and activities with the client
    result = await client.execute_workflow(
        CaptureTarget.run,
        target_name,
        id=f"bounty-hunter-workflow-{target_name}",
        task_queue=CAPTURE_TARGET_TASK_QUEUE,
    )
    logger.info(f"Workflow: Target Recieved? {result}")


# if __name__ == "__main__":        
#     # Execute the workflow for each target
#     asyncio.run(execute_workflow(target_name="Al Capone"))


async def main():
    target_name_1 = "Jesse James"
    target_name_2 = "Butch Cassidy" 
    target_name_3 = "Billy the Kid"

    await asyncio.gather(
        execute_workflow(target_name=target_name_1),
        execute_workflow(target_name=target_name_2),
        execute_workflow(target_name=target_name_3),
    )

if __name__ == "__main__":    
    asyncio.run(main())

