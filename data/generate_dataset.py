"""
Synthetic User Financial Profile Generator

Generates realistic Indian investor profiles covering:
  - Young professionals (25-35)
  - Mid-career earners (35-45)
  - Pre-retirement savers (45-55)
  - Various income brackets (₹5L to ₹35L per annum)
  - Mix of risk profiles, loan situations, insurance coverage gaps

No external data source needed — 100% programmatically generated.
Run directly:  python data/generate_dataset.py
"""
from __future__ import annotations

import json
import random
from pathlib import Path

NAMES = [
    "Rahul Gupta", "Priya Sharma", "Amit Patel", "Neha Singh",
    "Vikram Reddy", "Sneha Joshi", "Kiran Kumar", "Anita Rao",
    "Suresh Iyer", "Meera Nair", "Rohan Mehta", "Deepa Thomas",
    "Arjun Verma", "Kavya Pillai", "Manish Agarwal", "Divya Bhat",
    "Sanjay Desai", "Pooja Saxena", "Nikhil Jain", "Ritu Chandra",
]

INCOME_BANDS = [
    40_000, 50_000, 60_000, 75_000,
    1_00_000, 1_20_000, 1_50_000, 2_00_000,
    2_50_000, 3_00_000,
]


def _weighted_choice(items: list, weights: list):
    return random.choices(items, weights=weights, k=1)[0]


def generate_profile(seed: int | None = None) -> dict:
    """Generate one realistic user financial profile."""
    if seed is not None:
        random.seed(seed)

    name = random.choice(NAMES) + f"_{seed or random.randint(100, 999)}"
    age = random.randint(25, 56)
    monthly_income = _weighted_choice(
        INCOME_BANDS,
        [5, 8, 10, 15, 18, 16, 12, 8, 5, 3],
    )
    expense_ratio = random.uniform(0.45, 0.75)
    monthly_expenses = int(monthly_income * expense_ratio)
    retirement_age = _weighted_choice([55, 58, 60, 65], [20, 25, 40, 15])
    risk_profile = _weighted_choice(
        ["conservative", "moderate", "aggressive"],
        [25, 55, 20],
    )

    # Emergency fund (0–12 months; many Indians under-save here)
    ef_months = _weighted_choice([0, 1, 2, 3, 6, 9, 12], [10, 10, 15, 20, 25, 15, 5])
    emergency_fund = monthly_expenses * ef_months

    # Existing savings / investments
    max_savings = monthly_income * 24
    existing_savings = random.randint(0, max_savings)
    equity_share = random.uniform(0.30, 0.70)
    equity_investments = int(existing_savings * equity_share)
    debt_investments = existing_savings - equity_investments

    # Insurance policies
    insurance_policies: list[dict] = []
    if random.random() > 0.40:   # 60% have some term cover
        cover_mult = _weighted_choice([3, 5, 8, 10, 15], [10, 25, 30, 25, 10])
        insurance_policies.append({
            "type": "term",
            "cover": monthly_income * 12 * cover_mult,
            "premium": int(monthly_income * 0.008),
        })
    if random.random() > 0.35:   # 65% have some health cover
        health_cover = _weighted_choice(
            [2_00_000, 3_00_000, 5_00_000, 10_00_000],
            [20, 35, 30, 15],
        )
        insurance_policies.append({
            "type": "health",
            "cover": health_cover,
            "premium": int(health_cover * 0.005),
        })
    if random.random() > 0.80:   # 20% have accident cover
        insurance_policies.append({
            "type": "accident",
            "cover": 50_00_000,
            "premium": 2500,
        })

    # Outstanding loans
    outstanding_loans: list[dict] = []
    if random.random() > 0.50 and age >= 28:   # 50% have home loan
        loan_balance = _weighted_choice(
            [10_00_000, 20_00_000, 35_00_000, 50_00_000, 75_00_000],
            [10, 25, 30, 25, 10],
        )
        emi = int(loan_balance * 0.0085)           # ~8.5% rate, 20yr approx
        outstanding_loans.append({
            "type": "home",
            "balance": loan_balance,
            "emi": emi,
            "rate_pct": 8.5,
            "annual_interest": int(loan_balance * 0.075),
        })
    if random.random() > 0.75:   # 25% have personal / car loan
        p_balance = random.randint(50_000, 5_00_000)
        outstanding_loans.append({
            "type": "personal",
            "balance": p_balance,
            "emi": int(p_balance * 0.025),
            "rate_pct": 14.0,
            "annual_interest": int(p_balance * 0.12),
        })

    # Life goals
    life_goals: list[dict] = []
    if random.random() > 0.45:   # child education goal
        life_goals.append({
            "name": "child_education",
            "amount": _weighted_choice(
                [15_00_000, 25_00_000, 40_00_000],
                [30, 50, 20],
            ),
            "years": random.randint(8, 18),
        })
    if random.random() > 0.60:   # home purchase
        life_goals.append({
            "name": "home_purchase",
            "amount": _weighted_choice(
                [50_00_000, 80_00_000, 1_20_00_000],
                [30, 45, 25],
            ),
            "years": random.randint(3, 10),
        })
    if random.random() > 0.70:   # international vacation
        life_goals.append({
            "name": "world_tour",
            "amount": random.randint(3_00_000, 10_00_000),
            "years": random.randint(2, 8),
        })

    return {
        "id": seed or random.randint(1000, 9999),
        "name": name,
        "age": age,
        "monthly_income": monthly_income,
        "monthly_expenses": monthly_expenses,
        "annual_income": monthly_income * 12,
        "retirement_age": retirement_age,
        "risk_profile": risk_profile,
        "existing_savings": existing_savings,
        "equity_investments": equity_investments,
        "debt_investments": debt_investments,
        "emergency_fund": emergency_fund,
        "dependents": random.randint(0, 3),
        "outstanding_loans": outstanding_loans,
        "insurance_policies": insurance_policies,
        "life_goals": life_goals,
    }


def generate_dataset(n: int = 50) -> list[dict]:
    """Generate n synthetic user profiles with reproducible seeds."""
    return [generate_profile(seed=i) for i in range(1, n + 1)]


if __name__ == "__main__":
    profiles = generate_dataset(50)
    out = Path(__file__).parent / "sample_profiles.json"
    out.write_text(json.dumps(profiles, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Generated {len(profiles)} profiles → {out}")

    # Quick stats
    incomes = [p["monthly_income"] for p in profiles]
    ages = [p["age"] for p in profiles]
    print(f"   Income range: ₹{min(incomes):,} – ₹{max(incomes):,}/month")
    print(f"   Age range: {min(ages)} – {max(ages)}")
    print(f"   Risk profiles: { {r: sum(1 for p in profiles if p['risk_profile']==r) for r in ['conservative','moderate','aggressive']} }")
