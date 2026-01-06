from typing import Tuple
from .schemas import RoutedQuery

INTENT_KEYWORDS = {
    "Billing": ["refund", "invoice", "billing", "payment", "price", "charge"],
    "Technical Issue": ["error", "bug", "issue", "crash", "slow", "loading"],
    "Account & Subscription": ["login", "password", "account", "subscription", "plan", "cancel"],
    "Product Usage": ["how do i", "where can i", "feature", "use", "tutorial"],
    "General FAQ": ["what is acmecloud", "support hours", "contact", "help"],
}

DEFAULT_INTENT = "General FAQ"

def classify_intent(message: str) -> Tuple[str, float]:
    text = message.lower()
    best_intent = DEFAULT_INTENT
    best_score = 0.0

    for intent, keywords in INTENT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > best_score:
            best_score = score
            best_intent = intent

    confidence = min(1.0, best_score / 3.0)
    return best_intent, confidence

def route_query(message: str) -> RoutedQuery:
    intent, confidence = classify_intent(message)
    return RoutedQuery(
        user_message=message,
        intent=intent,
        confidence=confidence,
    )

if __name__ == "__main__":
    test_msg = "I was charged twice on my invoice, can I get a refund?"
    routed = route_query(test_msg)
    print(routed)
