"""
Financial Calculation Tools for FinSage

All tools are decorated with @tool so they can be:
  1. Called directly from agent node code (deterministic, demo mode)
  2. Bound to an LLM via llm.bind_tools(tools) for tool-calling (LLM mode)
  3. Used inside a LangGraph ToolNode for automatic tool execution

Demonstrates: LangChain @tool pattern + LangGraph ToolNode integration
"""

import math
from langchain_core.tools import tool


# ─── Tool 1: SIP Calculator ──────────────────────────────────────────────────

@tool
def calculate_sip_required(
    corpus_needed: float,
    years: int,
    expected_return_rate: float,
    existing_corpus: float = 0.0,
) -> dict:
    """Calculate the monthly SIP amount needed to reach a target corpus.

    Args:
        corpus_needed: Target corpus amount in INR.
        years: Number of years to achieve the goal.
        expected_return_rate: Annual expected return rate (e.g. 12 for 12%).
        existing_corpus: Existing savings that will compound (default 0).

    Returns:
        dict with monthly_sip, wealth_created, total_invested, and projections.
    """
    monthly_rate = expected_return_rate / 100 / 12
    n = years * 12

    # Future value of existing corpus
    fv_existing = existing_corpus * ((1 + monthly_rate) ** n)
    remaining_needed = max(0.0, corpus_needed - fv_existing)

    if monthly_rate == 0 or n == 0:
        sip = remaining_needed / max(n, 1)
    else:
        sip = remaining_needed * monthly_rate / (((1 + monthly_rate) ** n) - 1)

    return {
        "monthly_sip": round(sip),
        "corpus_target": round(corpus_needed),
        "years": years,
        "expected_return_pct": expected_return_rate,
        "fv_of_existing_corpus": round(fv_existing),
        "additional_corpus_needed": round(remaining_needed),
        "total_sip_invested": round(sip * n),
        "wealth_created": round(corpus_needed - sip * n - existing_corpus),
    }


# ─── Tool 2: Retirement Corpus Calculator ────────────────────────────────────

@tool
def calculate_retirement_corpus(
    current_monthly_expenses: float,
    current_age: int,
    retirement_age: int,
    life_expectancy: int = 85,
    inflation_rate: float = 6.0,
    post_retirement_return: float = 7.0,
) -> dict:
    """Calculate the corpus required for a comfortable retirement.

    Uses the inflation-adjusted annuity method:
      - Projects monthly expenses to retirement date using inflation
      - Applies real rate of return during drawdown phase

    Args:
        current_monthly_expenses: Current monthly expenses in INR.
        current_age: Current age of the user.
        retirement_age: Target retirement age.
        life_expectancy: Expected lifespan (default 85).
        inflation_rate: Annual inflation % (default 6).
        post_retirement_return: Portfolio return during retirement % (default 7).

    Returns:
        dict with corpus_required, corpus_in_crores, and breakdown.
    """
    years_to_retirement = max(1, retirement_age - current_age)
    retirement_years = max(1, life_expectancy - retirement_age)

    # Expenses at retirement (inflation adjusted)
    monthly_expenses_at_retirement = current_monthly_expenses * (
        (1 + inflation_rate / 100) ** years_to_retirement
    )
    annual_expenses_at_retirement = monthly_expenses_at_retirement * 12

    # Real return during retirement
    real_return = (1 + post_retirement_return / 100) / (1 + inflation_rate / 100) - 1

    if real_return > 0:
        corpus = annual_expenses_at_retirement * (
            1 - (1 + real_return) ** (-retirement_years)
        ) / real_return
    else:
        corpus = annual_expenses_at_retirement * retirement_years

    return {
        "corpus_required": round(corpus),
        "corpus_in_crores": round(corpus / 1_00_00_000, 2),
        "years_to_retirement": years_to_retirement,
        "retirement_years": retirement_years,
        "monthly_expenses_at_retirement": round(monthly_expenses_at_retirement),
        "annual_expenses_at_retirement": round(annual_expenses_at_retirement),
        "inflation_rate_pct": inflation_rate,
        "post_retirement_return_pct": post_retirement_return,
    }


# ─── Tool 3: Tax Liability Calculator ────────────────────────────────────────

@tool
def calculate_tax_liability(
    annual_income: float,
    deductions: dict,
    regime: str = "new",
) -> dict:
    """Calculate income tax liability under old or new Indian tax regime (FY 2024-25).

    Args:
        annual_income: Gross annual income in INR.
        deductions: Dict of section → amount, e.g. {"80C": 150000, "80D": 25000}.
                    (Only used for old regime.)
        regime: 'old' or 'new'.

    Returns:
        dict with taxable_income, total_tax, effective_rate, monthly_tax.
    """

    def _tax_on_slabs(income: float, slabs: list) -> float:
        tax = 0.0
        for lower, upper, rate in slabs:
            if income <= lower:
                break
            taxable = min(income, upper) - lower
            tax += taxable * rate / 100
        return tax

    std_deduction = 75_000 if regime == "new" else 50_000

    if regime == "new":
        taxable_income = max(0.0, annual_income - std_deduction)
        slabs = [
            (0, 300_000, 0),
            (300_000, 700_000, 5),
            (700_000, 1_000_000, 10),
            (1_000_000, 1_200_000, 15),
            (1_200_000, 1_500_000, 20),
            (1_500_000, math.inf, 30),
        ]
        deductions_applied = {"standard_deduction": std_deduction}
    else:
        total_deductions = std_deduction
        deductions_applied = {"standard_deduction": std_deduction}

        max_limits = {
            "80C": 150_000,
            "80D": 25_000,
            "80D_senior_parents": 50_000,
            "NPS_80CCD": 50_000,
            "home_loan_interest": 200_000,
            "80E": 1_000_000,   # education loan (no cap, capped at 10L for sanity)
            "80G": 500_000,     # donations
            "HRA": 600_000,     # HRA (simplified cap)
        }
        for section, amount in deductions.items():
            allowed = min(float(amount), max_limits.get(section, float(amount)))
            deductions_applied[section] = round(allowed)
            total_deductions += allowed

        taxable_income = max(0.0, annual_income - total_deductions)
        slabs = [
            (0, 250_000, 0),
            (250_000, 500_000, 5),
            (500_000, 1_000_000, 20),
            (1_000_000, math.inf, 30),
        ]

    base_tax = _tax_on_slabs(taxable_income, slabs)

    # Surcharge
    surcharge = 0.0
    if annual_income > 1_00_00_000:
        surcharge = base_tax * 0.15
    elif annual_income > 50_00_000:
        surcharge = base_tax * 0.10

    # Health & Education Cess (4%)
    cess = (base_tax + surcharge) * 0.04
    total_tax = base_tax + surcharge + cess

    # Rebate u/s 87A
    rebate_limit = 700_000 if regime == "new" else 500_000
    if annual_income <= rebate_limit:
        total_tax = 0.0

    return {
        "regime": regime,
        "gross_income": round(annual_income),
        "taxable_income": round(taxable_income),
        "deductions_applied": deductions_applied,
        "base_tax": round(base_tax),
        "surcharge": round(surcharge),
        "cess": round(cess),
        "total_tax": round(total_tax),
        "effective_rate_pct": round(total_tax / annual_income * 100, 2) if annual_income > 0 else 0,
        "monthly_tax": round(total_tax / 12),
    }


# ─── Tool 4: Financial Health Scorer ─────────────────────────────────────────

@tool
def calculate_financial_health_score(
    monthly_income: float,
    monthly_expenses: float,
    emergency_fund: float,
    total_debt_emi: float,
    total_savings: float,
    life_cover: float,
    health_cover: float,
    age: int,
) -> dict:
    """Score financial health across 6 dimensions (0-100 each) and return overall grade.

    Dimensions:
      1. Emergency Fund       — Benchmark: 6 months of expenses
      2. Insurance Coverage   — Life: 10x annual income; Health: ₹5L minimum
      3. Investment/Savings   — Benchmark: 20%+ savings rate
      4. Debt Health          — EMI-to-income ratio < 30%
      5. Tax Efficiency       — 80C utilisation proxy
      6. Retirement Readiness — Age-adjusted corpus ratio

    Returns:
        dict with scores per dimension, overall_score, grade (A-F), strengths, weaknesses.
    """
    scores: dict[str, float] = {}

    # 1. Emergency Fund
    required_ef = monthly_expenses * 6
    ef_ratio = emergency_fund / required_ef if required_ef > 0 else 0
    scores["emergency_fund"] = min(100.0, ef_ratio * 100)

    # 2. Insurance Coverage
    annual_income = monthly_income * 12
    life_ratio = life_cover / (annual_income * 10) if annual_income > 0 else 0
    health_ratio = health_cover / 500_000
    scores["insurance_coverage"] = min(100.0, life_ratio * 60 + health_ratio * 40)

    # 3. Investment/Savings Rate
    free_cash = monthly_income - monthly_expenses - total_debt_emi
    savings_rate = free_cash / monthly_income if monthly_income > 0 else 0
    if savings_rate >= 0.30:
        scores["investment_diversification"] = 100.0
    elif savings_rate >= 0.20:
        scores["investment_diversification"] = 75.0
    elif savings_rate >= 0.10:
        scores["investment_diversification"] = 50.0
    elif savings_rate >= 0:
        scores["investment_diversification"] = 25.0
    else:
        scores["investment_diversification"] = 0.0

    # 4. Debt Health (EMI/income)
    debt_ratio = total_debt_emi / monthly_income if monthly_income > 0 else 0
    if debt_ratio == 0:
        scores["debt_health"] = 100.0
    elif debt_ratio <= 0.20:
        scores["debt_health"] = 85.0
    elif debt_ratio <= 0.30:
        scores["debt_health"] = 65.0
    elif debt_ratio <= 0.40:
        scores["debt_health"] = 40.0
    else:
        scores["debt_health"] = 15.0

    # 5. Tax Efficiency (proxy: how much of 80C limit is used)
    scores["tax_efficiency"] = min(100.0, (total_savings / 150_000) * 100) if total_savings < 150_000 else 100.0

    # 6. Retirement Readiness (25x annual expenses rule, age-adjusted)
    years_to_60 = max(1, 60 - age)
    annual_expenses = monthly_expenses * 12
    ideal_corpus_now = annual_expenses * 25 * (1 - years_to_60 / 35)  # expected by now
    ideal_corpus_now = max(1, ideal_corpus_now)
    corpus_ratio = total_savings / ideal_corpus_now
    scores["retirement_readiness"] = min(100.0, corpus_ratio * 100)

    # Weighted overall score
    weights = {
        "emergency_fund": 0.20,
        "insurance_coverage": 0.25,
        "investment_diversification": 0.20,
        "debt_health": 0.15,
        "tax_efficiency": 0.10,
        "retirement_readiness": 0.10,
    }
    overall = sum(scores[k] * weights[k] for k in scores)
    grade = "A" if overall >= 80 else "B" if overall >= 65 else "C" if overall >= 50 else "D" if overall >= 35 else "F"

    return {
        "scores": {k: round(v, 1) for k, v in scores.items()},
        "overall_score": round(overall, 1),
        "grade": grade,
        "strengths": [k for k, v in scores.items() if v >= 70],
        "weaknesses": [k for k, v in scores.items() if v < 50],
        "savings_rate_pct": round(savings_rate * 100, 1),
        "emi_to_income_pct": round(debt_ratio * 100, 1),
    }


# ─── Tool 5: Asset Allocation Advisor ────────────────────────────────────────

@tool
def suggest_asset_allocation(age: int, risk_profile: str) -> dict:
    """Suggest optimal asset allocation based on age and risk profile.

    Uses the "100 − age" rule as a base, adjusted for risk appetite.

    Args:
        age: Current age.
        risk_profile: 'conservative', 'moderate', or 'aggressive'.

    Returns:
        dict with equity/debt/gold percentages and sub-allocation breakdown.
    """
    adjustments = {"conservative": -15, "moderate": 0, "aggressive": 12}
    base_equity = 100 - age
    equity = max(20.0, min(85.0, base_equity + adjustments.get(risk_profile, 0)))
    gold = 5.0
    debt = round(100.0 - equity - gold, 1)

    # Equity sub-allocation
    if equity > 60:
        lc, mc, sc, intl = 0.50, 0.30, 0.15, 0.05
    elif equity > 40:
        lc, mc, sc, intl = 0.60, 0.30, 0.10, 0.00
    else:
        lc, mc, sc, intl = 0.70, 0.25, 0.05, 0.00

    return {
        "equity_pct": round(equity, 1),
        "debt_pct": debt,
        "gold_pct": gold,
        "equity_breakdown": {
            "large_cap_funds": round(equity * lc, 1),
            "mid_cap_funds": round(equity * mc, 1),
            "small_cap_funds": round(equity * sc, 1),
            "international_funds": round(equity * intl, 1),
        },
        "debt_breakdown": {
            "ppf_epf": round(debt * 0.40, 1),
            "debt_mutual_funds": round(debt * 0.40, 1),
            "fixed_deposits": round(debt * 0.20, 1),
        },
        "rationale": (
            f"Age {age} with {risk_profile} profile → "
            f"Equity {equity}% for growth, Debt {debt}% for stability, Gold 5% as hedge."
        ),
    }


# ─── Tool 6: Insurance Requirement Calculator ────────────────────────────────

@tool
def calculate_insurance_requirement(
    monthly_income: float,
    age: int,
    dependents: int = 2,
    existing_life_cover: float = 0.0,
    existing_health_cover: float = 0.0,
) -> dict:
    """Calculate recommended insurance coverage and identify gaps.

    Life cover rule: 10-15x annual income (higher if young/many dependents).
    Health cover rule: ₹5L–₹10L based on age.

    Returns:
        dict with recommended covers, gaps, and estimated premiums.
    """
    annual_income = monthly_income * 12

    # Life coverage (10x base + 1x per additional dependent beyond 2)
    life_multiplier = 10 + max(0, dependents - 2)
    recommended_life = annual_income * life_multiplier
    life_gap = max(0.0, recommended_life - existing_life_cover)

    # Health coverage
    recommended_health = 1_000_000 if age >= 40 else 500_000
    health_gap = max(0.0, recommended_health - existing_health_cover)

    # Term premium estimate (₹10,000 per ₹1Cr cover at age 30, +5% per year)
    age_factor = 1 + max(0, age - 30) * 0.05
    term_premium_estimate = (life_gap / 1_00_00_000) * 10_000 * age_factor if life_gap > 0 else 0
    health_premium_estimate = health_gap * 0.003 if health_gap > 0 else 0

    return {
        "recommended_life_cover": round(recommended_life),
        "current_life_cover": round(existing_life_cover),
        "life_cover_gap": round(life_gap),
        "life_cover_gap_cr": round(life_gap / 1_00_00_000, 2),
        "recommended_health_cover": round(recommended_health),
        "current_health_cover": round(existing_health_cover),
        "health_cover_gap": round(health_gap),
        "estimated_term_premium_pa": round(term_premium_estimate),
        "estimated_health_premium_pa": round(health_premium_estimate),
        "total_additional_premium_pa": round(term_premium_estimate + health_premium_estimate),
        "adequately_covered": (life_gap == 0 and health_gap == 0),
    }


# ─── Exported tool list (used by ToolNode in graph.py) ───────────────────────

financial_tools = [
    calculate_sip_required,
    calculate_retirement_corpus,
    calculate_tax_liability,
    calculate_financial_health_score,
    suggest_asset_allocation,
    calculate_insurance_requirement,
]
