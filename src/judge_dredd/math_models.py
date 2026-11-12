"""EXPERIMENTAL: Mathematical utilities, not legal or moral verdicts."""
import math

def bradley_terry_probability(severity_a: float, severity_b: float) -> float:
    """P(prefer A over B) under a specified logistic latent-choice model."""
    z = severity_a - severity_b
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    ez = math.exp(z)
    return ez / (1.0 + ez)

def synthetic_severity(harm: float, intent: float, rights: float,
                       w_harm: float = .8, w_intent: float = 1.2,
                       w_rights: float = 1.0, interaction: float = .5) -> float:
    """Toy formula; value is NOT empirically calibrated MSU."""
    for name, value in {"harm": harm, "intent": intent, "rights": rights}.items():
        if not 0 <= value <= 1:
            raise ValueError(f"{name} must be between 0 and 1")
    return (w_harm * harm + w_intent * intent + w_rights * rights
            + interaction * harm * intent)
