import asyncio
from orchestrator import Orchestrator
# Import process_instruction from the new nlp_processor module
from nlp_processor import process_instruction
# Keep Action types imported as they are used within the workflow list type hint
from agent import Action
from typing import List, Any


async def main():
    """
    Main function to initialize the orchestrator, create an agent,
    process a natural language instruction into a workflow,
    execute the workflow, and shut down.
    """
    orchestrator = Orchestrator()
    agent = None  # Initialize agent to None for finally block

    try:
        # Initialize the orchestrator and launch the browser (headless=False to see the browser)
        await orchestrator.initialize(headless=True)
        print("Orchestrator initialized.")

        # Create an agent managed by the orchestrator
        agent = await orchestrator.create_agent()
        print("Agent created.")

        # --- Sample Natural Language Instruction ---
        # This instruction will be processed by the nlp_processor
        # instruction = "Go to https://www.wikipedia.org/"
        # Let's use a different page for variety
        instruction = "Go to https://www.wikipedia.org/wiki/Large_language_model"

        print(f"\n--- Processing Instruction: \"{instruction}\" ---")
        # Process the instruction to get a list of Action objects (the workflow)
        generated_workflow: List[Action] = process_instruction(instruction)

        if not generated_workflow:
            print("No actions generated from the instruction. Exiting.")
            return  # Exit if no valid workflow was generated

        print(
            f"Generated Workflow: {[action.description for action in generated_workflow]}")

        print("\n--- Starting Workflow Execution ---")
        # Execute the generated workflow using the created agent
        # Note: Currently, our simple processor only generates one action per instruction.
        # A more advanced processor would generate sequences.
        workflow_results = await orchestrator.execute_workflow_with_agent(agent, generated_workflow)

        print("\n--- Workflow Execution Results ---")
        for i, result in enumerate(workflow_results):
            print(f"Step {i+1} Result: {result}")
        print("----------------------------------")

    except Exception as e:
        print(f"\nAn error occurred during the main execution: {e}")
    finally:
        # Ensure orchestrator is shut down even if errors occur
        if orchestrator:
            await orchestrator.shutdown()
            print("\nOrchestrator has been shut down.")


if __name__ == "__main__":
    asyncio.run(main())
