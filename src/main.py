import time

from src.router.intent_router import route_query
from src.agents.billing_agent import handle_billing
from src.agents.tech_agent import handle_technical
from src.agents.account_agent import handle_account
from src.agents.product_agent import handle_product
from src.agents.general_agent import handle_general
from src.agents.escalation_agent import handle_escalation
from src.logging.logger import log_interaction


CONFIDENCE_THRESHOLD = 0.6


def dispatch_response(user_message: str) -> str:
    routed = route_query(user_message)
    intent = routed.intent
    confidence = routed.confidence

    fallback = False
    fallback_reason = None

    start = time.perf_counter()

    if confidence < CONFIDENCE_THRESHOLD:
        answer = handle_escalation(user_message, reason="low_confidence")
        fallback = True
        fallback_reason = "low_confidence"
        effective_intent = "Escalation"
    else:
        if intent == "Billing":
            answer = handle_billing(user_message)
        elif intent == "Technical Issue":
            answer = handle_technical(user_message)
        elif intent == "Account & Subscription":
            answer = handle_account(user_message)
        elif intent == "Product Usage":
            answer = handle_product(user_message)
        elif intent == "General FAQ":
            answer = handle_general(user_message)
        else:
            answer = handle_escalation(user_message, reason="unknown_intent")
            fallback = True
            fallback_reason = "unknown_intent"
            effective_intent = "Escalation"

        if not fallback:
            effective_intent = intent

    latency_ms = int((time.perf_counter() - start) * 1000)
    response_length = len(answer)

    log_interaction(
        {
            "user_message": user_message,
            "intent": effective_intent,
            "router_intent": intent,
            "confidence": confidence,
            "fallback": fallback,
            "fallback_reason": fallback_reason,
            "latency_ms": latency_ms,
            "response_length": response_length,
            "answer_preview": answer[:200],
        }
    )

    return answer


if __name__ == "__main__":
    msg = input("User: ")
    answer = dispatch_response(msg)
    print("\n" + answer)
