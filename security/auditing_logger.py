class AuditingLogger:
    """
    Logs security-relevant events and actions for auditing.
    """

    def __init__(self):
        self.logs = []

    def log_event(self, event: dict):
        """
        Records an event in the audit log.
        """
        self.logs.append(event)

    def get_logs(self, filter_by: dict = None):
        """
        Retrieves audit logs, optionally filtered.
        """
        return self.logs
