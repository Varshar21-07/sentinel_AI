def execute_action(action: str, ticket: str) -> str:
    """Mock execution of actions."""
    allowed = ["reset_password", "unlock_account", "check_status"]
    if action in allowed:
        return f"SUCCESS: Executed {action} for ticket."
    return f"ERROR: Action {action} is not recognized or not allowed for execution."
