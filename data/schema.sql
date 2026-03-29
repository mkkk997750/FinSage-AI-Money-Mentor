-- ============================================================
-- FinSage: AI Money Mentor — ET AI Hackathon 2026
-- PostgreSQL Schema
-- ============================================================

-- Drop existing tables in reverse FK order
DROP TABLE IF EXISTS conversation_history CASCADE;
DROP TABLE IF EXISTS agent_sessions CASCADE;
DROP TABLE IF EXISTS money_health_scores CASCADE;
DROP TABLE IF EXISTS couple_profiles CASCADE;
DROP TABLE IF EXISTS insurance_policies CASCADE;
DROP TABLE IF EXISTS life_events CASCADE;
DROP TABLE IF EXISTS tax_profiles CASCADE;
DROP TABLE IF EXISTS mutual_fund_holdings CASCADE;
DROP TABLE IF EXISTS financial_goals CASCADE;
DROP TABLE IF EXISTS financial_profiles CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ─────────────────────────────────────────────────────────────
-- 1. USERS
-- ─────────────────────────────────────────────────────────────
CREATE TABLE users (
    user_id          SERIAL PRIMARY KEY,
    name             VARCHAR(120) NOT NULL,
    email            VARCHAR(150) UNIQUE NOT NULL,
    phone            VARCHAR(15),
    city             VARCHAR(60),
    state            VARCHAR(60),
    age              INTEGER CHECK (age BETWEEN 18 AND 90),
    gender           VARCHAR(10),
    occupation       VARCHAR(120),
    employer         VARCHAR(150),
    marital_status   VARCHAR(20) CHECK (marital_status IN ('single','married','divorced','widowed')),
    dependents       INTEGER DEFAULT 0,
    created_at       TIMESTAMP DEFAULT NOW()
);

-- ─────────────────────────────────────────────────────────────
-- 2. FINANCIAL PROFILES
-- ─────────────────────────────────────────────────────────────
CREATE TABLE financial_profiles (
    profile_id               SERIAL PRIMARY KEY,
    user_id                  INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    monthly_income           NUMERIC(15,2) NOT NULL,
    monthly_expenses         NUMERIC(15,2) NOT NULL,
    monthly_savings          NUMERIC(15,2) GENERATED ALWAYS AS (monthly_income - monthly_expenses) STORED,
    emergency_fund           NUMERIC(15,2) DEFAULT 0,
    pf_balance               NUMERIC(15,2) DEFAULT 0,
    ppf_balance              NUMERIC(15,2) DEFAULT 0,
    fd_balance               NUMERIC(15,2) DEFAULT 0,
    stock_portfolio          NUMERIC(15,2) DEFAULT 0,
    mf_portfolio_value       NUMERIC(15,2) DEFAULT 0,
    real_estate_value        NUMERIC(15,2) DEFAULT 0,
    gold_value               NUMERIC(15,2) DEFAULT 0,
    nps_balance              NUMERIC(15,2) DEFAULT 0,
    home_loan_outstanding    NUMERIC(15,2) DEFAULT 0,
    car_loan_outstanding     NUMERIC(15,2) DEFAULT 0,
    personal_loan_outstanding NUMERIC(15,2) DEFAULT 0,
    credit_card_outstanding  NUMERIC(15,2) DEFAULT 0,
    monthly_emi              NUMERIC(15,2) DEFAULT 0,
    existing_life_cover      NUMERIC(15,2) DEFAULT 0,
    existing_health_cover    NUMERIC(15,2) DEFAULT 0,
    retirement_age           INTEGER DEFAULT 60,
    risk_profile             VARCHAR(20) CHECK (risk_profile IN ('conservative','moderate','aggressive')),
    updated_at               TIMESTAMP DEFAULT NOW()
);

-- ─────────────────────────────────────────────────────────────
-- 3. FINANCIAL GOALS
-- ─────────────────────────────────────────────────────────────
CREATE TABLE financial_goals (
    goal_id          SERIAL PRIMARY KEY,
    user_id          INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    goal_name        VARCHAR(120) NOT NULL,
    goal_type        VARCHAR(50) CHECK (goal_type IN ('retirement','education','house','car','vacation','emergency','marriage','business','other')),
    target_amount    NUMERIC(15,2) NOT NULL,
    current_savings  NUMERIC(15,2) DEFAULT 0,
    target_year      INTEGER,
    monthly_sip      NUMERIC(15,2) DEFAULT 0,
    priority         VARCHAR(10) CHECK (priority IN ('high','medium','low')),
    status           VARCHAR(20) CHECK (status IN ('on_track','behind','ahead','completed')) DEFAULT 'on_track',
    notes            TEXT,
    created_at       TIMESTAMP DEFAULT NOW()
);

-- ─────────────────────────────────────────────────────────────
-- 4. MUTUAL FUND HOLDINGS
-- ─────────────────────────────────────────────────────────────
CREATE TABLE mutual_fund_holdings (
    holding_id       SERIAL PRIMARY KEY,
    user_id          INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    fund_name        VARCHAR(200) NOT NULL,
    amc_name         VARCHAR(100),
    category         VARCHAR(60) CHECK (category IN ('Large Cap','Mid Cap','Small Cap','Flexi Cap','Hybrid','ELSS','Index','Debt','Sectoral','International')),
    folio_number     VARCHAR(60),
    units            NUMERIC(15,4),
    nav              NUMERIC(10,4),
    purchase_nav     NUMERIC(10,4),
    current_value    NUMERIC(15,2),
    invested_amount  NUMERIC(15,2),
    xirr             NUMERIC(8,2),
    expense_ratio    NUMERIC(6,4),
    monthly_sip      NUMERIC(15,2) DEFAULT 0,
    sip_start_date   DATE,
    benchmark        VARCHAR(150),
    created_at       TIMESTAMP DEFAULT NOW()
);

-- ─────────────────────────────────────────────────────────────
-- 5. TAX PROFILES
-- ─────────────────────────────────────────────────────────────
CREATE TABLE tax_profiles (
    tax_id                   SERIAL PRIMARY KEY,
    user_id                  INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    financial_year           VARCHAR(10) DEFAULT '2025-26',
    gross_salary             NUMERIC(15,2),
    hra_received             NUMERIC(15,2) DEFAULT 0,
    hra_exemption            NUMERIC(15,2) DEFAULT 0,
    lta                      NUMERIC(15,2) DEFAULT 0,
    section_80c              NUMERIC(15,2) DEFAULT 0,
    section_80d              NUMERIC(15,2) DEFAULT 0,
    section_80d_parents      NUMERIC(15,2) DEFAULT 0,
    nps_80ccd                NUMERIC(15,2) DEFAULT 0,
    home_loan_interest       NUMERIC(15,2) DEFAULT 0,
    section_80g              NUMERIC(15,2) DEFAULT 0,
    section_80e              NUMERIC(15,2) DEFAULT 0,
    other_deductions         NUMERIC(15,2) DEFAULT 0,
    old_regime_tax           NUMERIC(15,2),
    new_regime_tax           NUMERIC(15,2),
    recommended_regime       VARCHAR(10) CHECK (recommended_regime IN ('old','new')),
    tax_saved_if_switched    NUMERIC(15,2) DEFAULT 0,
    missed_deductions        TEXT,
    created_at               TIMESTAMP DEFAULT NOW()
);

-- ─────────────────────────────────────────────────────────────
-- 6. LIFE EVENTS
-- ─────────────────────────────────────────────────────────────
CREATE TABLE life_events (
    event_id         SERIAL PRIMARY KEY,
    user_id          INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    event_type       VARCHAR(60) CHECK (event_type IN ('marriage','baby','inheritance','bonus','job_change','home_purchase','vehicle_purchase','medical_emergency','retirement','business_start','education')),
    event_date       DATE,
    amount_involved  NUMERIC(15,2),
    description      TEXT,
    ai_recommendation TEXT,
    action_items     TEXT,
    status           VARCHAR(20) CHECK (status IN ('upcoming','recent','handled','pending')) DEFAULT 'upcoming',
    created_at       TIMESTAMP DEFAULT NOW()
);

-- ─────────────────────────────────────────────────────────────
-- 7. COUPLE PROFILES
-- ─────────────────────────────────────────────────────────────
CREATE TABLE couple_profiles (
    couple_id                    SERIAL PRIMARY KEY,
    partner1_user_id             INTEGER REFERENCES users(user_id),
    partner2_user_id             INTEGER REFERENCES users(user_id),
    combined_monthly_income      NUMERIC(15,2),
    combined_monthly_expenses    NUMERIC(15,2),
    combined_net_worth           NUMERIC(15,2),
    joint_hra_savings            NUMERIC(15,2) DEFAULT 0,
    recommended_nps_split        JSONB,
    recommended_sip_split        JSONB,
    joint_goals                  JSONB,
    insurance_gaps               TEXT,
    optimization_summary         TEXT,
    created_at                   TIMESTAMP DEFAULT NOW()
);

-- ─────────────────────────────────────────────────────────────
-- 8. INSURANCE POLICIES
-- ─────────────────────────────────────────────────────────────
CREATE TABLE insurance_policies (
    policy_id        SERIAL PRIMARY KEY,
    user_id          INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    policy_type      VARCHAR(40) CHECK (policy_type IN ('term_life','health','critical_illness','vehicle','home','ulip','endowment')),
    insurer_name     VARCHAR(100),
    policy_number    VARCHAR(60),
    sum_assured      NUMERIC(15,2),
    annual_premium   NUMERIC(15,2),
    cover_start_date DATE,
    cover_end_date   DATE,
    is_active        BOOLEAN DEFAULT TRUE,
    created_at       TIMESTAMP DEFAULT NOW()
);

-- ─────────────────────────────────────────────────────────────
-- 9. MONEY HEALTH SCORES
-- ─────────────────────────────────────────────────────────────
CREATE TABLE money_health_scores (
    score_id                    SERIAL PRIMARY KEY,
    user_id                     INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    overall_score               NUMERIC(5,2),
    grade                       VARCHAR(5),
    emergency_preparedness      NUMERIC(5,2),
    insurance_coverage          NUMERIC(5,2),
    investment_diversification  NUMERIC(5,2),
    debt_health                 NUMERIC(5,2),
    tax_efficiency              NUMERIC(5,2),
    retirement_readiness        NUMERIC(5,2),
    strengths                   TEXT,
    weaknesses                  TEXT,
    top_recommendations         TEXT,
    computed_at                 TIMESTAMP DEFAULT NOW()
);

-- ─────────────────────────────────────────────────────────────
-- 10. AGENT SESSIONS
-- ─────────────────────────────────────────────────────────────
CREATE TABLE agent_sessions (
    session_id   VARCHAR(60) PRIMARY KEY,
    user_id      INTEGER REFERENCES users(user_id),
    agent_type   VARCHAR(50),
    started_at   TIMESTAMP DEFAULT NOW(),
    last_active  TIMESTAMP DEFAULT NOW(),
    is_active    BOOLEAN DEFAULT TRUE,
    summary      TEXT
);

-- ─────────────────────────────────────────────────────────────
-- 11. CONVERSATION HISTORY
-- ─────────────────────────────────────────────────────────────
CREATE TABLE conversation_history (
    message_id   SERIAL PRIMARY KEY,
    session_id   VARCHAR(60) REFERENCES agent_sessions(session_id),
    role         VARCHAR(20) CHECK (role IN ('user','assistant','system','tool')),
    content      TEXT,
    agent_node   VARCHAR(60),
    metadata     JSONB,
    created_at   TIMESTAMP DEFAULT NOW()
);

-- ─────────────────────────────────────────────────────────────
-- Indexes for performance
-- ─────────────────────────────────────────────────────────────
CREATE INDEX idx_fp_user      ON financial_profiles(user_id);
CREATE INDEX idx_fg_user      ON financial_goals(user_id);
CREATE INDEX idx_mfh_user     ON mutual_fund_holdings(user_id);
CREATE INDEX idx_tp_user      ON tax_profiles(user_id);
CREATE INDEX idx_le_user      ON life_events(user_id);
CREATE INDEX idx_ip_user      ON insurance_policies(user_id);
CREATE INDEX idx_mhs_user     ON money_health_scores(user_id);
CREATE INDEX idx_ch_session   ON conversation_history(session_id);
CREATE INDEX idx_as_user      ON agent_sessions(user_id);
