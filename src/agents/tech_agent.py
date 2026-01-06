def handle_technical(query: str) -> str:
    return (
        "Technical Support Agent:\n"
        "Looks like you are facing a technical issue.\n"
        "Typically we would check system status, logs, and recent deployments for AcmeCloud."
    )
from src.tools.kb_search import search_kb

def handle_technical(query: str) -> str:
    matches = search_kb("technical.md", query, top_k=1)
    kb_text = matches[0][1] if matches else "No exact FAQ match was found."

    return (
        "Technical Support Agent (KB-backed):\n"
        f"User question: {query}\n\n"
        "Most relevant technical FAQ:\n"
        f"{kb_text}\n"
    )
