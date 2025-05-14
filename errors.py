class BitAgentError(Exception):
    """Base exception for all BitAgent related errors."""
    pass


class BrowserInteractionError(BitAgentError):
    """Raised when an error occurs during browser interaction (e.g., navigation, clicking)."""

    def __init__(self, message: str, url: str = None, selector: str = None):
        self.message = message
        self.url = url
        self.selector = selector
        super().__init__(self.message)

    def __str__(self):
        details = f"URL: {self.url}" if self.url else ""
        details += f", Selector: {self.selector}" if self.selector else ""
        return f"BrowserInteractionError: {self.message} ({details})"


class AgentExecutionError(BitAgentError):
    """Raised when an error occurs during agent action execution."""

    def __init__(self, message: str, action_description: str):
        self.message = message
        self.action_description = action_description
        super().__init__(self.message)

    def __str__(self):
        return f"AgentExecutionError: {self.message} during action '{self.action_description}'"


class WorkflowExecutionError(BitAgentError):
    """Raised when an error occurs during workflow execution."""

    def __init__(self, message: str, step_index: int, action_description: str):
        self.message = message
        self.step_index = step_index
        self.action_description = action_description
        super().__init__(self.message)

    def __str__(self):
        return f"WorkflowExecutionError: {self.message} at step {self.step_index+1} ({self.action_description})"


class NLPProcessingError(BitAgentError):
    """Raised when an error occurs during natural language instruction processing."""

    def __init__(self, message: str, instruction: str):
        self.message = message
        self.instruction = instruction
        super().__init__(self.message)

    def __str__(self):
        return f"NLPProcessingError: {self.message} for instruction '{self.instruction}'"

# We can add more specific exceptions as needed, e.g., ParsingError, AntiCrawlerError, etc.
