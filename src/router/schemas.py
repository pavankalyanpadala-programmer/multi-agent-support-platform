from dataclasses import dataclass

@dataclass
class RoutedQuery:
    user_message: str
    intent: str
    confidence: float
