import asyncio, random
from temporalio import activity
from globals import logger

logger.name = "quests"

@activity.defn
async def accept_bounty(target_name: str) -> bool:
    """
    This function is a placeholder for the actual implementation of bounty aceptance.
    """
    logger.info(f"***********Bounty for Target {target_name} accepted***********")    
    return True


@activity.defn
async def find_target(target_name: str):
    """
    This function is a placeholder for the actual implementation of finding a target.
    It simulates a delay and then returns a target.
    """
    await asyncio.sleep(1)
    logger.info(f"Looking for Target {target_name}" )


@activity.defn
async def is_target_alive(target_name: str) -> bool:
    """
    This function is a placeholder for the actual implementation of checking if a target is dead or alive.
    It simulates a delay and then returns a boolean indicating the target's status.
    The function uses a random number generator to simulate a 50% chance of the target being alive.
    """
    logger.info(f"Checking if target is alive: {target_name}...")
    
    # Simulate some processing time
    await asyncio.sleep(1)

    if random.random() < 0.9:
        # Simulate a high chance of the target being alive
        logger.info(f"Target {target_name} is alive")
        return True
    else:
        logger.info(f"Target {target_name} is dead")
        return False


@activity.defn
async def capture_target(target_name: str) -> bool:
    """
    This function is a placeholder for the actual implementation of capturing a target.
    It simulates a delay and then returns the captured target.
    """
    logger.info(f"Fighting started to capture target {target_name}...")
    
    # Simulate some processing time
    await asyncio.sleep(1)

    # Simulate a 10% chance of capturing the target        
    if random.random() < 0.5:
        # Simulate a chance of capturing the target
        logger.info(f"Target {target_name} injured and captured")
        return True
    else:
        logger.info(f"Target {target_name} Escaped, looking for the target again..")
        raise Exception(f"Target {target_name} escaped")


@activity.defn
async def return_target(target_name: str) -> bool:
    """
    This function is a placeholder for the actual implementation of returning a target.
    It simulates a delay and then returns the returned target.
    """
    # Simulate some processing time
    await asyncio.sleep(1)

    logger.info(f"------------Target {target_name} locked-up. Mission over------------")
    return True
