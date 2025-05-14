from playwright.async_api import Page, Locator
from typing import List, Dict, Any, Optional

# Define a simple structure to represent a parsed DOM element


class ParsedElement:
    def __init__(self, selector: str, tag: str, attributes: Dict[str, str], text_content: str, bounds: Optional[Dict[str, float]] = None):
        self.selector = selector  # Store the selector used to find this element
        self.tag = tag
        self.attributes = attributes
        self.text_content = text_content.strip() if text_content else ""
        self.bounds = bounds  # Optional: stores bounding box information

    def __repr__(self):
        return f"ParsedElement(tag='{self.tag}', selector='{self.selector}', text='{self.text_content[:50]}...')")

            async def parse_elements_by_selector(page: Page, selector: str) -> List[ParsedElement]:
            """
    Parses elements matching a CSS selector on the page and returns a list of ParsedElement objects.

    Args:
        page: The Playwright Page object.
        selector: The CSS selector for the elements to parse.

    Returns:
        A list of ParsedElement objects for the matching elements.
        Returns an empty list if no elements match.
    """
    parsed_elements: List[ParsedElement] = []
            try:
        # Use page.locator to find all elements matching the selector
        elements = page.locator(selector)
        count = await elements.count()

        if count == 0:
            print(f"No elements found for selector: {selector}")
            return []

        print(f"Found {count} elements for selector: {selector}. Parsing...")

        for i in range(count):
            element = elements.nth(i)
            # Get attributes as a dictionary
            attributes = await element.evaluate("el => { const attrs = {}; for (let i = 0; i < el.attributes.length; i++) { attrs[el.attributes[i].name] = el.attributes[i].value; } return attrs; }")
            tag = await element.evaluate("el => el.tagName")
            text_content = await element.text_content()

            # Optional: Get bounding box
            try:
                bounds = await element.bounding_box()
            except Exception:
                bounds = None # Bounding box might not be available for all element types

            parsed_elements.append(ParsedElement(
                # Store a specific selector for this instance
                selector=f"{selector}:nth-of-type({i+1})",
                tag=tag.lower() if tag else "",
                attributes=attributes if attributes else {},
                text_content=text_content if text_content else "",
                bounds=bounds
            ))

        print(f"Successfully parsed {len(parsed_elements)} elements.")
        return parsed_elements

            except Exception as e:
        # In a real scenario, use a specific parsing error from errors.py
        print(
           f"An error occurred during DOM parsing for selector {selector}: {e}")
            return []  # Return empty list on error for now, or raise a custom exception


                # Example Usage (commented out)
                # async def example_dom_parsing():
                #     from playwright.async_api import async_playwright
                #     from web_interaction import navigate_to_url # Assuming web_interaction is in the parent directory or PYTHONPATH
                #     import asyncio
                #
                #     async with async_playwright() as p:
                #         browser = await p.chromium.launch(headless=True)
                #         page = await browser.new_page()
                #
                #         try:
                #             await navigate_to_url(page, "https://example.com")
                #             # Parse all paragraph elements
                #             paragraphs = await parse_elements_by_selector(page, "p")
                #             print("\nParsed Paragraphs:")
                #             for p_element in paragraphs:
                #                 print(p_element)
                #
                #             # Parse all link elements
                #             links = await parse_elements_by_selector(page, "a")
                #             print("\nParsed Links:")
                #             for link_element in links:
                #                 print(link_element)
                #
                #         except Exception as e:
                #             print(f"Example DOM parsing failed: {e}")
                #         finally:
                #             await browser.close()
                #
                # if __name__ == "__main__":
                #     asyncio.run(example_dom_parsing())
