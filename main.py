import asyncio
from orchestrator import Orchestrator
from agent import NavigateAction, ExtractAction, ClickAction, TypeAction, Action
from typing import List, Any


async def main():
    """
    Main function to initialize the orchestrator, create an agent,
    define and execute a workflow, and shut down.
    """
    orchestrator = Orchestrator()
    try:
        # Initialize the orchestrator and launch the browser (headless=False to see the browser)
        await orchestrator.initialize(headless=True)

        # Create an agent managed by the orchestrator
        agent = await orchestrator.create_agent()

        # --- Define a simple test workflow ---
        # Example: Navigate to a page and extract a heading
        test_workflow: List[Action] = [
            NavigateAction(url="https://www.wikipedia.org/",
                           wait_for_selector="#main-page-content"),
            ExtractAction(selector="#main-page-content h1"),
            NavigateAction(
                url="https://www.wikipedia.org/wiki/Artificial_intelligence"),
            ExtractAction(selector="#firstHeading")
            # Add more actions as needed, e.g.:
            # ClickAction(selector="..."),
            # TypeAction(selector="..."),
        ]
        # -----------------------------------

        print("\n--- Starting Workflow Execution ---")
        # Execute the workflow using the created agent
        workflow_results = await orchestrator.execute_workflow_with_agent(agent, test_workflow)

        print("\n--- Workflow Execution Results ---")
        for i, result in enumerate(workflow_results):
            print(f"Step {i+1} Result: {result}")
        print("----------------------------------")

    except Exception as e:
        print(f"\nAn error occurred during the main execution: {e}")
    finally:
        # Ensure orchestrator is shut down even if errors occur
        await orchestrator.shutdown()
        print("\nOrchestrator has been shut down.")


if __name__ == "__main__":
    asyncio.run(main())
