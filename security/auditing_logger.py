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
        return True

    def get_logs(self, filter_by: dict = None):
        """
        Retrieves audit logs, optionally filtered.
        """
        if filter_by:
            # Simple filter: all key-value pairs in filter_by must match
            return [log for log in self.logs if all(log.get(k) == v for k, v in filter_by.items())]
        return self.logs
