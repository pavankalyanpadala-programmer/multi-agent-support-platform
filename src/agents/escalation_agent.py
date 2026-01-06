def handle_escalation(query: str, reason: str = "manual") -> str:
    return (
        "Escalation Agent:\n"
        f"This conversation is being handed to a human agent (reason: {reason}).\n"
        "A human support specialist would review the full context and respond."
    )
