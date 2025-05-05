## Bounty Hunter Game with Temporal Python SDK
Python app leveraging Temporal SDK to demonstrate temporal capabilities

I’ve built a simple **Bounty Hunter** game in Python that uses [Temporal's Python SDK](https://docs.temporal.io/docs/python/introduction) to orchestrate a series of quests—each represented as a workflow activity, including:
- `accept_bounty`
- `find_target`
- `is_target_alive`
- `capture_target`
- `return_target`

Each activity depends on the successful completion of the previous one and may also rely on external systems.

The quest progression is defined in `gameflow.py`, with **state management handled by Temporal**. This ensures that if the game crashes or a user exits mid-session, it can resume from the last checkpoint.

### Handling External Dependencies
The game also demonstrates how to handle external dependencies—such as waiting for user input or signals from third-party services—using **Temporal signals**. For instance, the workflow listens for a `"target_spotted"` signal to proceed once the target has been identified.

### Key Temporal Features Demonstrated
- **Timeouts**: Manage delays or unresponsive activities  
- **Signals**: Integrate asynchronous external inputs  
- **Retries**: Automatically retry failed activities to handle exceptions and ensure robustness

### Instructions
1. Install dependencies
2. Run temporal server (temporal server start-dev)
3. Open the UI at: http://localhost:8233/namespaces/default/workflows
4. Run the "run_gameflow.py" file
5. Run the "run_worker.py" file
