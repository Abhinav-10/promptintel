from decimal import Decimal


def normalize_outcome(outcome_value: Decimal) -> Decimal:
    if outcome_value <= 0:
        return Decimal("0")
    if outcome_value >= 1000:
        return Decimal("100")
    return outcome_value / Decimal("10")


def calculate_prompt_score(*, rating: int, reuse_count: int, outcome_value: Decimal) -> Decimal:
    rating_component = (Decimal(rating) / Decimal("5")) * Decimal("40")
    reuse_component = min(Decimal(reuse_count) * Decimal("5"), Decimal("20"))
    outcome_component = min(normalize_outcome(outcome_value) * Decimal("0.4"), Decimal("40"))

    return (rating_component + reuse_component + outcome_component).quantize(Decimal("0.01"))