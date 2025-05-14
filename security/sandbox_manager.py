class SandboxManager:
    """
    Manages browser sandboxing and process isolation for security.
    """

    def __init__(self):
        self.sandboxes = {}

    def create_sandbox(self, agent_id: str):
        """
        Creates a new sandbox environment for an agent.
        """
        self.sandboxes[agent_id] = f"sandbox_for_{agent_id}"
        return self.sandboxes[agent_id]

    def destroy_sandbox(self, agent_id: str):
        """
        Destroys the sandbox environment for an agent.
        """
        if agent_id in self.sandboxes:
            del self.sandboxes[agent_id]
            return True
        return False

    def list_sandboxes(self):
        """
        Returns a list of active sandboxes.
        """
        return list(self.sandboxes.keys())
