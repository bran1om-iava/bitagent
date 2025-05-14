from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError


async def navigate_to_url(page: Page, url: str, wait_for_selector: str = None):
    """
    Navigates the given page to a URL and optionally waits for a selector.

    Args:
        page: The Playwright Page object.
        url: The URL to navigate to.
        wait_for_selector: An optional CSS selector to wait for after navigation.
                           If None, the function waits for the 'load' event.

    Raises:
        PlaywrightTimeoutError: If navigation or waiting for the selector times out.
        Exception: For other potential navigation errors.
    """
    try:
        print(f"Navigating to {url}...")
        # Wait for the 'load' event by default
        await page.goto(url, wait_until="load")

        if wait_for_selector:
            print(f"Waiting for selector: {wait_for_selector}")
            # Using state='attached' or 'visible' is often more reliable than default
            await page.wait_for_selector(wait_for_selector, state='attached')
            print(f"Selector found: {wait_for_selector}")

        print(f"Successfully navigated to {url}")

    except PlaywrightTimeoutError as e:
        print(f"Navigation or waiting for selector timed out: {e}")
        raise
    except Exception as e:
        print(f"An error occurred during navigation: {e}")
        raise


async def extract_element_text(page: Page, selector: str) -> str | None:
    """
    Extracts the text content from the first element matching the selector.

    Args:
        page: The Playwright Page object.
        selector: The CSS selector for the element.

    Returns:
        The text content of the element, or None if the element is not found.
    """
    try:
        print(f"Attempting to extract text from selector: {selector}")
        # Using locator and first() to target the first matching element
        element = page.locator(selector).first
        # Check if the element exists before trying to get text
        if await element.count() > 0:
            text = await element.text_content()
            print(f"Successfully extracted text from {selector}")
            return text.strip() if text else ""
        else:
            print(f"Element not found for selector: {selector}")
            return None
    except Exception as e:
        print(f"An error occurred while extracting text: {e}")
        # Depending on requirements, we might raise the exception or return None
        return None


async def click_element(page: Page, selector: str):
    """
    Clicks the first element matching the selector.

    Args:
        page: The Playwright Page object.
        selector: The CSS selector for the element.

    Raises:
        PlaywrightTimeoutError: If the element is not found within the timeout.
        Exception: For other potential clicking errors.
    """
    try:
        print(f"Attempting to click element with selector: {selector}")
        # Using locator and click for robust clicking
        await page.locator(selector).first.click()
        print(f"Successfully clicked element with selector: {selector}")
    except PlaywrightTimeoutError as e:
        print(
            f"Element not found or clickable within timeout for selector: {selector} - {e}")
        raise
    except Exception as e:
        print(f"An error occurred while clicking element: {e}")
        raise


async def type_text(page: Page, selector: str, text: str):
    """
    Types text into the first input element matching the selector.

    Args:
        page: The Playwright Page object.
        selector: The CSS selector for the input element.
        text: The text to type.

    Raises:
        PlaywrightTimeoutError: If the element is not found within the timeout.
        Exception: For other potential typing errors.
    """
    try:
        print(f"Attempting to type into element with selector: {selector}")
        # Using locator and fill for typing into input fields
        await page.locator(selector).first.fill(text)
        print(f"Successfully typed into element with selector: {selector}")
    except PlaywrightTimeoutError as e:
        print(
            f"Element not found or fillable within timeout for selector: {selector} - {e}")
        raise
    except Exception as e:
        print(f"An error occurred while typing into element: {e}")
        raise
