from playwright.async_api import Browser, Page
from web_interaction import navigate_to_url, extract_element_text, click_element, type_text
from typing import Any, Dict, Optional

# --- Action Definitions ---


class Action:
    """Base class for all agent actions."""

    def __init__(self, description: str):
        self.description = description

    async def execute(self, page: Page) -> Any:
        """Executes the action on the given page."""
        raise NotImplementedError(
            "Subclasses must implement the execute method")


class NavigateAction(Action):
    """Action to navigate to a specific URL."""

    def __init__(self, url: str, wait_for_selector: Optional[str] = None, description: str = None):
        super().__init__(description or f"Navigate to {url}")
        self.url = url
        self.wait_for_selector = wait_for_selector

    async def execute(self, page: Page) -> None:
        await navigate_to_url(page, self.url, self.wait_for_selector)


class ExtractAction(Action):
    """Action to extract text from an element."""

    def __init__(self, selector: str, description: str = None):
        super().__init__(
            description or f"Extract text from selector {selector}")
        self.selector = selector

    async def execute(self, page: Page) -> str | None:
        return await extract_element_text(page, self.selector)


class ClickAction(Action):
    """Action to click an element."""

    def __init__(self, selector: str, description: str = None):
        super().__init__(
            description or f"Click element with selector {selector}")
        self.selector = selector

    async def execute(self, page: Page) -> None:
        await click_element(page, self.selector)


class TypeAction(Action):
    """Action to type text into an element."""

    def __init__(self, selector: str, text: str, description: str = None):
        super().__init__(
            description or f"Type '{text}' into element with selector {selector}")
        self.selector = selector
        self.text = text

    async def execute(self, page: Page) -> None:
        await type_text(page, self.selector, self.text)

# --- Agent Definition ---


class Agent:
    """
    A base class for an AI Agent capable of interacting with web pages.
    Manages its own browser page and executes a sequence of Actions.
    """

    def __init__(self, browser: Browser):
        self.browser = browser
        self.page: Page = None  # Agent will manage its own page

    async def initialize(self):
        """Initializes the agent's browser page."""
        if self.page is None:
            self.page = await self.browser.new_page()
            print(f"Agent initialized with a new page.")
        else:
            print("Agent already initialized.")

    async def close(self):
        """Closes the agent's browser page."""
        if self.page is not None:
            await self.page.close()
            self.page = None
            print("Agent page closed.")

    async def perform_task(self, action: Action) -> Any:
        """
        Performs a single action using the agent's page.

        Args:
            action: An Action object representing the task.

        Returns:
            Any: The result of the action, if any (e.g., extracted text).
        """
        if self.page is None:
            print(
                f"Agent not initialized. Cannot perform action: {action.description}")
            return None

        print(f"Agent performing action: {action.description}")
        try:
            result = await action.execute(self.page)
            print(f"Action completed: {action.description}")
            return result
        except Exception as e:
            print(f"Action failed: {action.description} - {e}")
            raise  # Re-raise the exception for higher-level handling

    async def execute_workflow(self, workflow: list[Action]) -> list[Any]:
        """
        Executes a sequence of actions as a workflow.

        Args:
            workflow: A list of Action objects.

        Returns:
            list[Any]: A list of results from executing each action.
        """
        if self.page is None:
            await self.initialize()

        results = []
        try:
            for i, action in enumerate(workflow):
                print(
                    f"Executing step {i+1}/{len(workflow)}: {action.description}")
                result = await self.perform_task(action)
                results.append(result)
            print("Workflow completed.")
        except Exception as e:
            print(
                f"Workflow execution failed at step {i+1}: {action.description}")
            # Depending on requirements, we might stop or continue on error
            raise
        finally:
            # Decide if the page should be closed after a workflow
            # await self.close()
            pass  # Keep the page open for further interactions if needed


# Example usage (commented out)
# async def example_agent_workflow():
#     from playwright.async_api import async_playwright
#     async with async_playwright() as p:
#         # Launch browser outside the agent to potentially share among agents or manage centrally
#         browser = await p.chromium.launch()
#         agent = Agent(browser)
#
#         # Define a simple workflow
#         search_workflow = [
#             NavigateAction(url="https://www.google.com", wait_for_selector='textarea[name="q"]'),
#             TypeAction(selector='textarea[name="q"]', text='Playwright github'),
#             ClickAction(selector='input[value="Google Search"]'), # This might need adjustment based on actual Google page structure
#             # Assuming navigation to search results page happens and h3 is a good selector for result titles
#             # A real workflow might need a wait here, e.g., page.wait_for_url(...)
#             # ExtractAction(selector="h3") # Selector for search result title might vary
#         ]
#
#         try:
#             print("Starting example agent workflow...")
#             results = await agent.execute_workflow(search_workflow)
#             print("\nWorkflow results:")
#             for result in results:
#                 print(f"- {result}")
#
#         except Exception as e:
#             print(f"\nExample workflow failed: {e}")
#         finally:
#             await agent.close()
#             await browser.close()
#
# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(example_agent_workflow())
