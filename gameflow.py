import asyncio
from temporalio import workflow
from quests import accept_bounty, find_target, is_target_alive, capture_target, return_target
from temporalio.common import RetryPolicy
from datetime import timedelta
from globals import logger

# This module defines the workflow for capturing a target.
# It orchestrates the process of finding, checking, capturing, and returning a target.
# It uses Temporal's workflow and activity features to manage the execution flow and handle retries.

logger.name = "gameflow"

@workflow.defn
class CaptureTarget:

    def __init__(self):
        self.target_spotted_event = asyncio.Event()

    @workflow.run
    async def run(self, target_name: str) -> bool:
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=2),
            maximum_interval=timedelta(seconds=10),
            backoff_coefficient=2.0,
            maximum_attempts=3,
            # non_retryable_error_types=["Exception"],            
        )


        await workflow.execute_activity(
            accept_bounty,
            target_name,
            start_to_close_timeout=timedelta(seconds=5)
        )


        await workflow.execute_activity(
            find_target,
            target_name,
            start_to_close_timeout=timedelta(seconds=5)
        )


        logger.info(f"Waiting for target to be spotted...")
        bounty_timeout = timedelta(seconds=30)
 
        try:
            await asyncio.wait_for(self.target_spotted_event.wait(), timeout=bounty_timeout.total_seconds())
        except asyncio.TimeoutError:
            logger.info(f"Bounty expired: target not spotted in time")
            logger.info(f"***********You Lost, Bounty for {target_name} Cancelled.***********\n")
            return False
        logger.info("Target spotted...heading to capture.")

        alive = await workflow.execute_activity(
            is_target_alive,
            target_name,
            start_to_close_timeout=timedelta(seconds=5)
        )
        if not alive:
            logger.info(f"***********Target {target_name} is dead. Bounty Gone***********")
            return False


        try:
            await workflow.execute_activity(
                capture_target,
                target_name,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=retry_policy
            )
        except Exception as e:
            logger.info(f"*********You Lost, {target_name} Escaped*********")
            return False


        returned = await workflow.execute_activity(
            return_target,
            target_name,
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=retry_policy
        )
        if not returned:
            logger.info(f"Failed to return target {target_name}.")
            return False

        logger.info(f"***********Bounty for {target_name} Collected.***********\n")
        return True

    # Signal handler for when the target is spotted
    @workflow.signal
    async def target_spotted(self):
        logger.info("Signal Received: Target spotted. Heading to capture.")
        self.target_spotted_event.set()

