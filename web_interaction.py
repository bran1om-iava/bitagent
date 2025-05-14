from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError
from typing import List, Any, Optional
import asyncio
# Import custom error classes
from errors import BrowserInteractionError


async def navigate_to_url(page: Page, url: str, wait_for_selector: Optional[str] = None):
    """
    Navigates the given page to a URL and optionally waits for a selector.

    Args:
        page: The Playwright Page object.
        url: The URL to navigate to.
        wait_for_selector: An optional CSS selector to wait for after navigation.
                           If None, the function waits for the 'load' event.

    Raises:
        BrowserInteractionError: If navigation or waiting for the selector fails or times out.
    """
    try:
        print(f"Navigating to {url}...")
        # Wait for the 'load' event by default
        # Added a default timeout
        await page.goto(url, wait_until="load", timeout=60000)

        if wait_for_selector:
            print(f"Waiting for selector: {wait_for_selector}")
            # Using state='attached' or 'visible' is often more reliable than default
            # Added a default timeout
            await page.wait_for_selector(wait_for_selector, state='attached', timeout=30000)
            print(f"Selector found: {wait_for_selector}")

        print(f"Successfully navigated to {url}")

    except PlaywrightTimeoutError as e:
        raise BrowserInteractionError(
            f"Navigation or waiting for selector timed out: {e}", url=url, selector=wait_for_selector)
    except Exception as e:
        # Catching other potential errors during navigation
        raise BrowserInteractionError(
            f"An unexpected error occurred during navigation: {e}", url=url)


async def extract_element_text(page: Page, selector: str) -> str | None:
    """
    Extracts the text content from the first element matching the selector.

    Args:
        page: The Playwright Page object.
        selector: The CSS selector for the element.

    Returns:
        The text content of the element, or None if the element is not found.

    Raises:
        BrowserInteractionError: If an unexpected error occurs during text extraction.
    """
    try:
        print(f"Attempting to extract text from selector: {selector}")
        # Using locator and first() to target the first matching element
        element = page.locator(selector).first
        # Check if the element exists before trying to get text
        # Using locator.count() is a quick way to check existence without strict waiting
        if await element.count() > 0:
            text = await element.text_content()
            print(f"Successfully extracted text from {selector}")
            return text.strip() if text else ""
        else:
            print(f"Element not found for selector: {selector}")
            return None
    except Exception as e:
        # Catching other potential errors during extraction
        raise BrowserInteractionError(
            f"An unexpected error occurred while extracting text: {e}", selector=selector)


async def click_element(page: Page, selector: str):
    """
    Clicks the first element matching the selector.

    Args:
        page: The Playwright Page object.
        selector: The CSS selector for the element.

    Raises:
        BrowserInteractionError: If the element is not found or clickable within the timeout, or another error occurs.
    """
    try:
        print(f"Attempting to click element with selector: {selector}")
        # Using locator and click for robust clicking - Playwright waits for element to be visible and clickable
        # Added a default timeout
        await page.locator(selector).first.click(timeout=30000)
        print(f"Successfully clicked element with selector: {selector}")
    except PlaywrightTimeoutError as e:
        raise BrowserInteractionError(
            f"Element not found or clickable within timeout: {e}", selector=selector)
    except Exception as e:
        # Catching other potential errors during clicking
        raise BrowserInteractionError(
            f"An unexpected error occurred while clicking element: {e}", selector=selector)


async def type_text(page: Page, selector: str, text: str):
    """
    Types text into the first input element matching the selector.

    Args:
        page: The Playwright Page object.
        selector: The CSS selector for the input element.
        text: The text to type.

    Raises:
        BrowserInteractionError: If the element is not found or fillable within the timeout, or another error occurs.
    """
    try:
        print(f"Attempting to type into element with selector: {selector}")
        # Using locator and fill for typing into input fields - Playwright waits for element to be visible and editable
        # Added a default timeout
        await page.locator(selector).first.fill(text, timeout=30000)
        print(f"Successfully typed into element with selector: {selector}")
    except PlaywrightTimeoutError as e:
        raise BrowserInteractionError(
            f"Element not found or fillable within timeout: {e}", selector=selector)
    except Exception as e:
        # Catching other potential errors during typing
        raise BrowserInteractionError(
            f"An unexpected error occurred while typing into element: {e}", selector=selector)


async def extract_table_data(page: Page, selector: str) -> List[List[str]] | None:
    """
    Extracts data from the first HTML table matching the selector.

    Args:
        page: The Playwright Page object.
        selector: The CSS selector for the table element.

    Returns:
        A list of lists representing the table data, or None if the table is not found.

    Raises:
        BrowserInteractionError: If an unexpected error occurs during table extraction.
    """
    try:
        print(
            f"Attempting to extract data from table with selector: {selector}")
        table_element = page.locator(selector).first

        # Using locator.count() to check existence
        if await table_element.count() == 0:
            print(f"Table not found for selector: {selector}")
            return None

        data: List[List[str]] = []
        # Using locator to find rows within the table element
        rows = table_element.locator("tr")

        for i in range(await rows.count()):
            row_element = rows.nth(i)
            # Using locator to find cells (th or td) within each row
            cells = row_element.locator("th, td")
            row_data: List[str] = []
            for j in range(await cells.count()):
                cell_element = cells.nth(j)
                text = await cell_element.text_content()
                row_data.append(text.strip() if text else "")
            data.append(row_data)

        print(
            f"Successfully extracted data from table with selector: {selector}")
        return data

    except Exception as e:
        # Catching other potential errors during table extraction
        raise BrowserInteractionError(
            f"An unexpected error occurred while extracting table data: {e}", selector=selector)


async def take_screenshot(page: Page, path: str) -> None:
    """
    Takes a screenshot of the current page and saves it to a file.

    Args:
        page: The Playwright Page object.
        path: The file path to save the screenshot (e.g., "screenshot.png").

    Raises:
        BrowserInteractionError: If an error occurs while taking the screenshot.
    """
    try:
        print(f"Attempting to take screenshot and save to {path}")
        await page.screenshot(path=path)
        print(f"Screenshot saved successfully to {path}")
    except Exception as e:
        raise BrowserInteractionError(
            f"An error occurred while taking screenshot: {e}", url=page.url)


async def handle_dialog(page: Page, accept: bool = True, prompt_text: Optional[str] = None) -> None:
    """
    Handles a dialog (alert, confirm, prompt) that appears on the page.

    Args:
        page: The Playwright Page object.
        accept: Whether to accept (True) or dismiss (False) the dialog.
                Defaults to True.
        prompt_text: The text to enter if the dialog is a prompt. Only used if accept is True.

    Raises:
        BrowserInteractionError: If an error occurs while setting up or handling the dialog.
    """
    try:
        # Playwright automatically dismisses dialogs by default unless a handler is attached.
        # We attach a one-time handler here.
        # Use page.once to ensure the handler is removed after the first dialog.
        page.once("dialog", lambda dialog: asyncio.create_task(
            _handle_specific_dialog(dialog, accept, prompt_text)))
        print("Dialog handler registered.")
        # Note: The dialog event is emitted as soon as the dialog appears.
        # The action that caused the dialog to appear should be called before this handler is needed.
    except Exception as e:
        raise BrowserInteractionError(
            f"An error occurred while setting up dialog handler: {e}", url=page.url)


async def _handle_specific_dialog(dialog, accept: bool, prompt_text: Optional[str]) -> None:
    """Internal helper to handle the specific dialog instance."""
    try:
        print(
            f"Dialog appeared - type: {dialog.type}, message: {dialog.message}")
        if accept:
            print("Accepting dialog.")
            if dialog.type == "prompt" and prompt_text is not None:
                await dialog.accept(prompt_text)
            else:
                await dialog.accept()
        else:
            print("Dismissing dialog.")
            await dialog.dismiss()
    except Exception as e:
        # Error during dialog handling itself
        print(f"An error occurred while handling the specific dialog: {e}")
        # We might not re-raise here as the main flow might have moved on,
        # but logging is important.


# Example usage (for testing purposes - commented out)
# async def example_web_interaction_errors():
#     from playwright.async_api import async_playwright
#     async with async_playwright() as p:
#         browser = await p.chromium.launch()
#         page = await browser.new_page()
#         try:
#             # Example of a navigation error (invalid URL)
#             await navigate_to_url(page, "invalid-url")
#         except BrowserInteractionError as e:
#             print(f"\nCaught expected error: {e}")
#
#         try:
#             # Example of a selector not found error
#             await navigate_to_url(page, "https://example.com")
#             await extract_element_text(page, ".non-existent-selector")
#         except BrowserInteractionError as e:
#              # This won't be caught by BrowserInteractionError from extract_element_text
#              # because extract_element_text returns None if not found, not raises an error
#              # Need to adjust extract_element_text if we want it to raise on not found.
#              pass # Update: extract_element_text now returns None as originally designed.
#
#         try:
#             # Example of a click error (element not interactable or not found within Playwright's click timeout)
#              await navigate_to_url(page, "https://example.com")
#              await click_element(page, ".non-existent-button")
#         except BrowserInteractionError as e:
#             print(f"Caught expected error: {e}")
#
#         finally:
#             await browser.close()
#
# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(example_web_interaction_errors())
