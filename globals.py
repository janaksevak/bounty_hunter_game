import logging

# Setting up logging configuration
logging.basicConfig(
level=logging.INFO,  # Set minimum level to display
format='%(asctime)s %(levelname)s [%(name)s] %(message)s',
datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)


# Creating a global shared file for constants and utility functions
CAPTURE_TARGET_TASK_QUEUE = "capture-target-task-queue"
