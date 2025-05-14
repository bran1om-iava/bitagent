from typing import List, Dict, Any, Optional, Union
from playwright.async_api import Page
from parsing.dom_parser import ParsedElement, parse_elements_by_selector
from parsing.semantic_parser import SemanticElement, parse_page_semantics
# from errors import DataExtractionError # To be defined in errors.py


class ExtractionQuery:
    """
    Defines what data to extract. Can be based on selectors, semantic roles, or patterns.
    """

    def __init__(self, query_type: str, value: str, target_attribute: Optional[str] = None, is_regex: bool = False):
        # query_type: 'selector', 'semantic_role', 'text_pattern'
        self.query_type = query_type
        self.value = value  # e.g., CSS selector, role name like 'button', regex pattern
        # e.g., 'href' for a link, 'text_content', or a specific attribute from SemanticAttribute
        self.target_attribute = target_attribute
        self.is_regex = is_regex  # If value is a regex pattern for text_pattern type

    def __repr__(self):
        return f"ExtractionQuery(type='{self.query_type}', value='{self.value}', target='{self.target_attribute}')"


async def extract_data_from_elements(elements: List[Union[ParsedElement, SemanticElement]], query: ExtractionQuery) -> List[Any]:
    """
    Extracts data from a list of ParsedElement or SemanticElement objects based on an ExtractionQuery.

    Args:
        elements: A list of elements to process.
        query: The ExtractionQuery defining what to extract.

    Returns:
        A list of extracted data points. The type of data depends on the query.
    """
    extracted_data: List[Any] = []

    for element in elements:
        try:
            match = False
            data_to_extract = None

            if query.query_type == 'selector':  # This case is more about filtering elements, actual extraction is below
                # This query type is typically handled by parse_elements_by_selector beforehand.
                # If elements are already ParsedElement, we assume they match the selector implicitly.
                # If they are SemanticElement, they were derived from ParsedElement.
                match = True

            elif query.query_type == 'semantic_role' and isinstance(element, SemanticElement):
                if element.semantic_role == query.value:
                    match = True

            elif query.query_type == 'text_pattern':
                # This would typically apply to element.text_content
                # For simplicity, this example doesn't implement regex matching here yet.
                # It assumes text_content is the target for pattern matching.
                pass  # Placeholder for regex matching on text_content

            # If the element matches the query type and value (or if it's a general extraction from pre-filtered elements)
            if match:
                if query.target_attribute == 'text_content':
                    data_to_extract = element.text_content
                elif query.target_attribute and hasattr(element, 'attributes') and query.target_attribute in element.attributes:
                    data_to_extract = element.attributes.get(
                        query.target_attribute)
                elif query.target_attribute and isinstance(element, SemanticElement):
                    # Check semantic attributes if the target is not a direct DOM attribute
                    for sem_attr in element.semantic_attributes:
                        if sem_attr.name == query.target_attribute:
                            data_to_extract = sem_attr.value
                            break
                elif not query.target_attribute:  # If no target attribute, maybe return the element itself or a summary
                    # Default to string representation
                    data_to_extract = str(element)

            if data_to_extract is not None:
                extracted_data.append(data_to_extract)

        except Exception as e:  # Replace with specific DataExtractionError
            print(
                f"Error extracting data for query '{query}' from element '{element}': {e}")

    return extracted_data


async def extract_data_from_page(page: Page, queries: List[ExtractionQuery]) -> Dict[str, List[Any]]:
    """
    Orchestrates data extraction from a page based on a list of queries.

    Args:
        page: The Playwright Page object.
        queries: A list of ExtractionQuery objects.

    Returns:
        A dictionary where keys are query descriptions (or values) and values are lists of extracted data.
    """
    results: Dict[str, List[Any]] = {}

    # For simplicity, this example processes queries sequentially and might re-parse elements.
    # A more optimized version would parse all relevant elements once, then apply queries.
    # Or, have a two-pass: first get all ParsedElements, then semantically enhance, then extract.

    for i, query in enumerate(queries):
        # Unique key for results
        query_key = f"{query.query_type}_{query.value}_{query.target_attribute or 'default'}_{i}"
        try:
            if query.query_type == 'selector':
                # Get raw DOM elements first
                raw_elements = await parse_elements_by_selector(page, query.value)
                # Then extract based on target_attribute from these raw elements
                results[query_key] = await extract_data_from_elements(raw_elements, query)

            elif query.query_type == 'semantic_role':
                # This is more complex: requires getting all relevant elements, then semantic parsing, then filtering & extracting.
                # For a simpler first pass, let's assume we operate on ALL elements of the page, then filter.
                # This is inefficient but demonstrates the flow.
                # A better way: parse_elements_by_selector for a broad selector (e.g., 'body *' or specific containers)
                print(
                    f"Semantic role query: '{query.value}'. Consider pre-filtering with a selector for efficiency.")
                # Example: get all elements in body
                all_parseable_elements = await parse_elements_by_selector(page, 'body *')
                if not all_parseable_elements:
                    results[query_key] = []
                    continue

                semantic_elements = await parse_page_semantics(all_parseable_elements)
                results[query_key] = await extract_data_from_elements(semantic_elements, query)

            # elif query.query_type == 'text_pattern':
            #     # Similar to semantic_role, would need to get elements, then apply regex.
            #     # results[query_key] = await extract_by_text_pattern(page, query.value, query.target_attribute, query.is_regex)
            #     pass
            else:
                print(f"Unsupported query type: {query.query_type}")
                results[query_key] = []

        except Exception as e:  # Replace with DataExtractionError
            print(f"Failed to execute extraction query '{query}': {e}")
            results[query_key] = [f"Error: {e}"]

    return results

# Example Usage (Conceptual)
# async def example_data_extraction():
#     from playwright.async_api import async_playwright
#     import asyncio
#
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)
#         page = await browser.new_page()
#         try:
#             await page.goto("https://example.com")
#             print("Navigated to example.com")
#
#             queries = [
#                 ExtractionQuery(query_type='selector', value='h1', target_attribute='text_content'),
#                 ExtractionQuery(query_type='selector', value='a', target_attribute='href'),
#                 ExtractionQuery(query_type='semantic_role', value='link', target_attribute='link_url'),
#                 ExtractionQuery(query_type='semantic_role', value='heading', target_attribute='text_content')
#             ]
#
#             extracted_content = await extract_data_from_page(page, queries)
#             print("\nExtracted Data:")
#             for key, data_list in extracted_content.items():
#                 print(f"  Query ({key}):")
#                 for item in data_list:
#                     print(f"    - {item}")
#
#         except Exception as e:
#             print(f"Data extraction example failed: {e}")
#         finally:
#             await browser.close()
#
# if __name__ == "__main__":
#     # asyncio.run(example_data_extraction())
#     print("Data extractor module loaded. Run example_data_extraction() to test.")
#     pass
