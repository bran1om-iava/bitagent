class AntiCrawlerStrategies:
    """
    Implements anti-crawler evasion techniques for browser automation.
    """

    def __init__(self):
        self.strategies = ["stealth_mode",
                           "random_user_agent", "delay_actions"]

    def apply_strategy(self, page, strategy_name: str):
        """
        Applies a named anti-crawler strategy to a browser page.
        """
        if strategy_name not in self.strategies:
            raise ValueError(f"Strategy {strategy_name} not found.")
        # Mock: just print what would be done
        print(f"Applying {strategy_name} to page {page}")
        return True

    def list_strategies(self):
        """
        Lists available anti-crawler strategies.
        """
        return self.strategies
