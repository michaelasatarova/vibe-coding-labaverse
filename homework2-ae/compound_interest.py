import math


def compound_interest(principal: float, rate: float, time: float, n: int = 1) -> float:
    """Calculate compound interest using standard or continuous compounding.

    Args:
        principal: Initial investment (P), must be non-negative.
        rate: Annual interest rate as a decimal (e.g., 0.05 for 5%).
        time: Duration in years, must be non-negative.
        n: Compounding periods per year (default 1). Pass None or 0 for continuous compounding.

    Returns:
        Final amount A after compounding.
    """
    if principal < 0:
        raise ValueError(f"Principal must be non-negative, got {principal}")
    if time < 0:
        raise ValueError(f"Time must be non-negative, got {time}")

    # Continuous compounding: A = Pe^(rt)
    if not n:
        return principal * math.exp(rate * time)

    # Standard compounding: A = P(1 + r/n)^(nt)
    return principal * (1 + rate / n) ** (n * time)


if __name__ == "__main__":
    # Standard: monthly compounding for 10 years at 5%
    amount = compound_interest(principal=1000, rate=0.05, time=10, n=12)
    print(f"Standard (monthly):    ${amount:.2f}")  # $1647.01

    # Continuous compounding
    amount_cont = compound_interest(principal=1000, rate=0.05, time=10, n=None)
    print(f"Continuous:            ${amount_cont:.2f}")  # $1648.72
