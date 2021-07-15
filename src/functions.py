from enum import Enum
from typing import List, Tuple

from software20 import optimize
from software20.typing import Identity, Cluster, OrderedEnum


@optimize
def detect_spam(text: str) -> bool:
    ...


@detect_spam.parser
def _(datum: str) -> Tuple[str, bool]:
    target, text = datum.split("\t")
    return [text], target == "spam"


class NewsCategory(Enum):
    SPORTS = 1
    POLITICS = 2
    SCIENCE = 3


@optimize
def classify_news_article(text: str) -> NewsCategory:
    ...


@optimize
def predict_temperature(past_temperatures: List[float]) -> float:
    ...


class RiskLevel(OrderedEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

@optimize
def predict_risk_level(smoker: bool, past_smoker: bool, has_allergies: bool) -> RiskLevel:
    ...


@optimize
def autoencode_text(text: str) -> Identity[str]:
    ...

@optimize
def cluster_text(text: str) -> Cluster:
    ...
