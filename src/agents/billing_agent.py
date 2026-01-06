def handle_billing(query: str) -> str:
    return (
        "Billing Agent:\n"
        "I see a billing-related question.\n"
        "For AcmeCloud, refunds and duplicate charges are usually resolved within 5–7 business days.\n"
        "If this were production, I would check your latest invoice and create a refund ticket."
    )
from src.tools.kb_search import search_kb

def handle_billing(query: str) -> str:
    matches = search_kb("billing.md", query, top_k=1)
    kb_text = matches[0][1] if matches else "No exact FAQ match was found."

    return (
        "Billing Agent (KB-backed):\n"
        f"User question: {query}\n\n"
        "Most relevant billing FAQ:\n"
        f"{kb_text}\n"
    )
