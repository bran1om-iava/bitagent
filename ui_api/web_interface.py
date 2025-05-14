class WebInterface:
    """
    Web-based user interface for interacting with the agent system.
    """

    def __init__(self):
        self.server_running = False

    def start_server(self, host: str = '0.0.0.0', port: int = 8000):
        """
        Starts the web server.
        """
        self.server_running = True
        print(f"Web server started at http://{host}:{port}")
        # Mock: just print, no real server
        return True

    def handle_request(self, request):
        """
        Handles a web request.
        """
        print(f"Handling web request: {request}")
        return {"status": "ok", "request": request}
