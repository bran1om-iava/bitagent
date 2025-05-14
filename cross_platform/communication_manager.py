class CommunicationManager:
    """
    Manages inter-process and inter-agent communication.
    """

    def __init__(self):
        self.inbox = []

    def send_message(self, recipient_id: str, message: dict):
        """
        Sends a message to another agent or process.
        """
        # Mock: just print the message
        print(f"Sending message to {recipient_id}: {message}")
        return True

    def receive_message(self):
        """
        Receives a message for this agent or process.
        """
        # Mock: pop from inbox if available
        if self.inbox:
            return self.inbox.pop(0)
        return None
