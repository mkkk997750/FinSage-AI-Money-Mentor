-- ============================================================
-- FinSage Seed Data — Realistic Indian Financial Profiles
-- ET AI Hackathon 2026
-- ============================================================

-- ─────────────────────────────────────────────────────────────
-- USERS (25 rows)
-- ─────────────────────────────────────────────────────────────
INSERT INTO users (name, email, phone, city, state, age, gender, occupation, employer, marital_status, dependents) VALUES
('Rahul Sharma',       'rahul.sharma@gmail.com',      '9876543210', 'Bengaluru',         'Karnataka',          28, 'Male',   'Software Engineer',     'Infosys Ltd',              'single',  0),
('Priya Mehta',        'priya.mehta@gmail.com',       '9867452310', 'Mumbai',             'Maharashtra',        32, 'Female', 'Marketing Manager',     'HUL India',                'married', 1),
('Amit Patel',         'amit.patel@gmail.com',        '9845632100', 'Ahmedabad',          'Gujarat',            45, 'Male',   'Business Owner',        'Patel Textiles Pvt Ltd',   'married', 3),
('Anjali Singh',       'anjali.singh@gmail.com',      '9823412390', 'New Delhi',          'Delhi',              38, 'Female', 'Cardiologist',          'AIIMS Delhi',              'married', 2),
('Vikram Nair',        'vikram.nair@gmail.com',       '9811234567', 'Mumbai',             'Maharashtra',        35, 'Male',   'Investment Banker',     'Goldman Sachs India',      'married', 1),
('Sunita Kapoor',      'sunita.kapoor@gmail.com',     '9856781234', 'Jaipur',             'Rajasthan',          42, 'Female', 'Senior Teacher',        'Delhi Public School',      'married', 2),
('Ravi Gupta',         'ravi.gupta@gmail.com',        '9845671890', 'Hyderabad',          'Telangana',          30, 'Male',   'Chartered Accountant',  'Deloitte India',           'single',  0),
('Deepika Rao',        'deepika.rao@gmail.com',       '9876512340', 'Pune',               'Maharashtra',        29, 'Female', 'Product Manager',       'Zomato',                   'single',  0),
('Suresh Kumar',       'suresh.kumar@gmail.com',      '9834561230', 'Chennai',            'Tamil Nadu',         52, 'Male',   'Factory Supervisor',    'TVS Motors',               'married', 3),
('Kavita Joshi',       'kavita.joshi@gmail.com',      '9867341230', 'Noida',              'Uttar Pradesh',      36, 'Female', 'HR Manager',            'Wipro Technologies',       'married', 1),
('Arun Verma',         'arun.verma@gmail.com',        '9845129870', 'Lucknow',            'Uttar Pradesh',      27, 'Male',   'Sales Executive',       'Asian Paints',             'single',  0),
('Meera Iyer',         'meera.iyer@gmail.com',        '9823456780', 'Bengaluru',          'Karnataka',          31, 'Female', 'Data Scientist',        'Flipkart',                 'single',  0),
('Rajesh Nair',        'rajesh.nair@gmail.com',       '9856123490', 'Kochi',              'Kerala',             44, 'Male',   'Civil Engineer',        'L&T Construction',         'married', 2),
('Pooja Agarwal',      'pooja.agarwal@gmail.com',     '9867891230', 'New Delhi',          'Delhi',              26, 'Female', 'Fashion Designer',      'NIFT Startup',             'single',  0),
('Sanjay Khanna',      'sanjay.khanna@gmail.com',     '9812345670', 'Chandigarh',         'Punjab',             60, 'Male',   'Retired Govt Officer',  'Retired (IAS)',            'married', 1),
('Natasha DSouza',     'natasha.dsouza@gmail.com',    '9876543100', 'Mumbai',             'Maharashtra',        33, 'Female', 'Senior Journalist',     'Times of India',           'single',  0),
('Karthik Sundaram',   'karthik.sundaram@gmail.com',  '9845678012', 'Bengaluru',          'Karnataka',          37, 'Male',   'Startup Founder',       'TechSprint AI Pvt Ltd',    'married', 1),
('Rekha Pillai',       'rekha.pillai@gmail.com',      '9867542310', 'Thiruvananthapuram', 'Kerala',             48, 'Female', 'Bank Branch Manager',   'State Bank of India',      'married', 2),
('Mohit Srivastava',   'mohit.sriv@gmail.com',        '9823419870', 'Hyderabad',          'Telangana',          25, 'Male',   'Junior Software Dev',   'TCS',                      'single',  0),
('Lalitha Krishnan',   'lalitha.krishnan@gmail.com',  '9834512360', 'Chennai',            'Tamil Nadu',         40, 'Female', 'Freelance Consultant',  'Self Employed',            'married', 2),
('Arjun Mehta',        'arjun.mehta@gmail.com',       '9867452311', 'Mumbai',             'Maharashtra',        34, 'Male',   'Financial Analyst',     'HDFC Bank',                'married', 1),
('Geeta Patel',        'geeta.patel@gmail.com',       '9845632101', 'Ahmedabad',          'Gujarat',            42, 'Female', 'Homemaker',             'Home',                     'married', 3),
('Dr Rohan Singh',     'rohan.singh@gmail.com',       '9823412391', 'New Delhi',          'Delhi',              40, 'Male',   'Orthopaedic Surgeon',   'Max Hospital',             'married', 2),
('Nisha Nair',         'nisha.nair@gmail.com',        '9811234568', 'Mumbai',             'Maharashtra',        33, 'Female', 'Interior Designer',     'Nisha Designs Studio',     'married', 1),
('Ramesh Kapoor',      'ramesh.kapoor@gmail.com',     '9856781235', 'Jaipur',             'Rajasthan',          45, 'Male',   'Wholesale Trader',      'Kapoor Enterprises',       'married', 2);

-- ─────────────────────────────────────────────────────────────
-- FINANCIAL PROFILES (25 rows)
-- ─────────────────────────────────────────────────────────────
INSERT INTO financial_profiles
  (user_id, monthly_income, monthly_expenses, emergency_fund, pf_balance, ppf_balance, fd_balance,
   stock_portfolio, mf_portfolio_value, real_estate_value, gold_value, nps_balance,
   home_loan_outstanding, car_loan_outstanding, personal_loan_outstanding, credit_card_outstanding,
   monthly_emi, existing_life_cover, existing_health_cover, retirement_age, risk_profile) VALUES
(1,  120000, 62000,  360000,   288000,   50000,   100000,  450000,   380000,       0,          85000,   60000,   0,          420000,  0,         0,         12000,  10000000,  500000,  50, 'aggressive'),
(2,  85000,  55000,  220000,   408000,   72000,   50000,   200000,   650000,       0,          60000,   0,       0,          0,       150000,    12000,     8000,   5000000,   300000,  58, 'moderate'),
(3,  250000, 130000, 780000,   0,        150000,  2000000, 1500000,  3500000,      15000000,   500000,  0,       8500000,   0,       0,          0,         95000,  25000000,  1000000, 55, 'moderate'),
(4,  180000, 90000,  540000,   1440000,  200000,  500000,  800000,   1200000,      12000000,   300000,  360000,  0,          0,       0,          0,         0,      20000000,  1000000, 58, 'moderate'),
(5,  300000, 150000, 900000,   720000,   300000,  1000000, 5000000,  8000000,      20000000,   800000,  600000,  12000000,  800000,  0,          0,         105000, 30000000,  2000000, 55, 'aggressive'),
(6,  45000,  32000,  96000,    324000,   120000,  150000,  0,        120000,       3500000,    200000,  0,       2200000,   0,       0,          0,         25000,  3000000,   300000,  60, 'conservative'),
(7,  95000,  50000,  300000,   228000,   100000,  200000,  350000,   480000,       0,          100000,  95000,   0,          0,       0,          0,         0,      10000000,  500000,  55, 'moderate'),
(8,  110000, 65000,  325000,   264000,   30000,   50000,   180000,   520000,       0,          80000,   0,       0,          0,       100000,    25000,     8000,   5000000,   300000,  52, 'aggressive'),
(9,  55000,  45000,  90000,    792000,   50000,   200000,  0,        60000,        4000000,    150000,  0,       1800000,   120000,  0,          0,         18000,  2000000,   200000,  60, 'conservative'),
(10, 70000,  48000,  192000,   336000,   80000,   100000,  150000,   380000,       0,          120000,  70000,   0,          240000,  0,          0,         10000,  5000000,   300000,  58, 'moderate'),
(11, 38000,  30000,  60000,    54720,    0,        50000,   0,        30000,        0,          0,       0,       0,          0,       80000,     15000,     5000,   2000000,   200000,  60, 'conservative'),
(12, 140000, 70000,  420000,   336000,   100000,  100000,  600000,   920000,       0,          200000,  140000,  0,          0,       0,          0,         0,      10000000,  500000,  48, 'aggressive'),
(13, 80000,  55000,  165000,   576000,   150000,  300000,  200000,   450000,       5000000,    250000,  80000,   3500000,   360000,  0,          0,         48000,  8000000,   500000,  60, 'moderate'),
(14, 42000,  32000,  96000,    75600,    0,        30000,   0,        40000,        0,          50000,   0,       0,          0,       60000,     20000,     4000,   2000000,   200000,  60, 'moderate'),
(15, 28000,  22000,  264000,   5000000,  800000,  1500000, 500000,   2000000,      8000000,    600000,  0,       0,          0,       0,          0,         0,      10000000,  500000,  65, 'conservative'),
(16, 62000,  42000,  168000,   223200,   40000,   80000,   100000,   240000,       0,          60000,   0,       0,          0,       120000,    30000,     6000,   5000000,   300000,  58, 'moderate'),
(17, 200000, 100000, 600000,   0,        200000,  500000,  2000000,  4500000,      10000000,   400000,  200000,  6000000,   0,       0,          0,         50000,  20000000,  2000000, 50, 'aggressive'),
(18, 100000, 65000,  390000,   1440000,  200000,  500000,  300000,   800000,       5000000,    300000,  200000,  2500000,   0,       0,          0,         30000,  10000000,  1000000, 58, 'moderate'),
(19, 52000,  38000,  112000,   93600,    0,        20000,   50000,    80000,        0,          30000,   52000,   0,          0,       60000,     10000,     3500,   3000000,   200000,  60, 'moderate'),
(20, 15000,  12000,  36000,    0,        50000,    80000,   0,        120000,       3000000,    200000,  0,       0,          0,       0,          0,         0,      2000000,   300000,  65, 'conservative'),
(21, 170000, 80000,  480000,   816000,   150000,  300000,  800000,   1200000,      0,          200000,  170000,  0,          0,       0,          0,         0,      15000000,  1000000, 58, 'aggressive'),
(22, 8000,   7000,   24000,    0,        30000,    50000,   0,        80000,        3500000,    250000,  0,       0,          0,       0,          0,         0,      2000000,   300000,  65, 'conservative'),
(23, 400000, 180000, 1200000,  2880000,  500000,  1000000, 3000000,  5000000,      20000000,   500000,  800000,  8000000,   1200000, 0,          0,         120000, 40000000,  2000000, 58, 'aggressive'),
(24, 55000,  38000,  165000,   198000,   60000,   100000,  200000,   350000,       0,          100000,  0,       0,          180000,  0,          0,         8000,   5000000,   500000,  58, 'moderate'),
(25, 120000, 70000,  420000,   0,        200000,  800000,  500000,   600000,       8000000,    400000,  0,       0,          0,       0,          0,         0,      8000000,   500000,  60, 'moderate');

-- ─────────────────────────────────────────────────────────────
-- FINANCIAL GOALS (55 rows, ~2-3 per user)
-- ─────────────────────────────────────────────────────────────
INSERT INTO financial_goals (user_id, goal_name, goal_type, target_amount, current_savings, target_year, monthly_sip, priority, status, notes) VALUES
-- Rahul Sharma (1)
(1,  'Early Retirement Corpus',       'retirement',  30000000,  880000,   2048, 30000, 'high',   'on_track', 'Target FIRE by age 50'),
(1,  'International Vacation - Europe','vacation',    500000,    80000,    2026, 15000, 'medium', 'on_track', 'Euro trip in Dec 2026'),
(1,  'Emergency Fund Top-up',          'emergency',   600000,    360000,   2027, 10000, 'high',   'behind',   'Need 6 months expenses'),
-- Priya Mehta (2)
(2,  'Child Education Fund',           'education',   5000000,   320000,   2040, 12000, 'high',   'on_track', 'Daughter Riya - 3 yrs old'),
(2,  'Buy Own Flat in Mumbai',         'house',       15000000,  500000,   2032, 25000, 'high',   'behind',   'Prefer Powai or Thane'),
(2,  'Annual Goa Vacation',            'vacation',    150000,    20000,    2026, 8000,  'low',    'on_track', 'Family trip every year'),
-- Amit Patel (3)
(3,  'Retirement Corpus',              'retirement',  50000000,  5200000,  2036, 50000, 'high',   'ahead',    'Plan to retire at 55'),
(3,  'Children Higher Education',      'education',   10000000,  1500000,  2033, 30000, 'high',   'on_track', '3 children - staggered'),
(3,  'Business Expansion Capital',     'business',    20000000,  2000000,  2028, 80000, 'medium', 'on_track', 'New manufacturing unit'),
-- Anjali Singh (4)
(4,  'Retirement Corpus',              'retirement',  60000000,  2000000,  2047, 40000, 'high',   'on_track', 'Retire at 60 with comfort'),
(4,  'Children Education Abroad',      'education',   8000000,   800000,   2038, 20000, 'high',   'on_track', 'US/UK university target'),
(4,  'Second Home in Mussoorie',       'house',       8000000,   500000,   2030, 30000, 'medium', 'behind',   'Weekend/retirement home'),
-- Vikram Nair (5)
(5,  'Retirement Corpus',              'retirement',  100000000, 9800000,  2046, 80000, 'high',   'ahead',    'Target 10 Cr by 45, 20Cr by 55'),
(5,  'Child Education Fund',           'education',   10000000,  1200000,  2040, 25000, 'high',   'on_track', 'Son Aryan - 2 yrs old'),
(5,  'Luxury Vacation Europe-US',      'vacation',    1200000,   200000,   2027, 30000, 'low',    'on_track', 'Anniversary trip 2027'),
-- Sunita Kapoor (6)
(6,  'Daughter Marriage Fund',         'marriage',    2000000,   120000,   2030, 8000,  'high',   'behind',   'Daughters wedding fund'),
(6,  'Retirement Corpus',              'retirement',  8000000,   440000,   2040, 5000,  'high',   'behind',   'Retire at 60'),
(6,  'Son Education Fund',             'education',   2500000,   200000,   2032, 6000,  'medium', 'on_track', 'Son in class 6'),
-- Ravi Gupta (7)
(7,  'Early Retirement Corpus',        'retirement',  25000000,  903000,   2052, 35000, 'high',   'behind',   'FIRE at 55'),
(7,  'Own Home in Hyderabad',          'house',       8000000,   400000,   2030, 20000, 'high',   'on_track', 'Madhapur or Kondapur area'),
(7,  'International MBA Abroad',       'education',   4000000,   200000,   2028, 15000, 'medium', 'behind',   'Considering ISB or abroad'),
-- Deepika Rao (8)
(8,  'Early Retirement - FIRE',        'retirement',  40000000,  750000,   2046, 30000, 'high',   'on_track', 'Retire at 45'),
(8,  'Buy Flat in Pune',               'house',       7000000,   300000,   2030, 20000, 'high',   'behind',   'Hinjewadi or Wakad area'),
(8,  'Startup Capital',                'business',    2000000,   125000,   2028, 15000, 'medium', 'on_track', 'EdTech startup idea'),
-- Suresh Kumar (9)
(9,  'Retirement Corpus',              'retirement',  5000000,   852000,   2034, 5000,  'high',   'behind',   'Simple retirement at 60'),
(9,  'Daughter Marriage Fund',         'marriage',    1500000,   100000,   2030, 5000,  'high',   'behind',   'Elder daughter marriage'),
-- Kavita Joshi (10)
(10, 'Retirement Corpus',              'retirement',  15000000,  600000,   2044, 10000, 'high',   'on_track', 'Retire at 58'),
(10, 'Son Engineering College Fund',  'education',   3000000,   200000,   2032, 8000,  'high',   'on_track', 'IIT/NIT target'),
(10, 'Family Vacation Thailand',       'vacation',    200000,    30000,    2027, 6000,  'low',    'on_track', 'Family trip 2027'),
-- Arun Verma (11)
(11, 'Emergency Fund',                 'emergency',   180000,    60000,    2027, 5000,  'high',   'behind',   '6 months expenses'),
(11, 'Honda City Car',                 'car',         1200000,   50000,    2028, 10000, 'medium', 'behind',   'First car target'),
-- Meera Iyer (12)
(12, 'FIRE Corpus',                    'retirement',  60000000,  1360000,  2042, 60000, 'high',   'on_track', 'Retire at 42'),
(12, 'Flat in Bengaluru',              'house',       10000000,  500000,   2029, 30000, 'high',   'on_track', 'Whitefield or Indiranagar'),
(12, 'PhD Abroad',                     'education',   3000000,   300000,   2028, 10000, 'medium', 'ahead',    'Considering Stanford/MIT'),
-- Rajesh Nair (13)
(13, 'Retirement Corpus',              'retirement',  20000000,  1006000,  2037, 15000, 'high',   'behind',   'Retire at 55'),
(13, 'Children Education Fund',        'education',   5000000,   400000,   2036, 10000, 'high',   'on_track', 'Both children education'),
-- Pooja Agarwal (14)
(14, 'Own Studio Setup',               'business',    800000,    90000,    2027, 15000, 'high',   'on_track', 'Design studio in Delhi'),
(14, 'Foreign Education - Fashion',    'education',   3000000,   70000,    2028, 12000, 'medium', 'behind',   'Parsons / RCA London'),
-- Sanjay Khanna (15)
(15, 'Spouse Healthcare Fund',         'other',       2000000,   2800000,  2030, 0,     'high',   'ahead',    'Medical corpus for wife'),
(15, 'Pilgrimage Travel Fund',         'vacation',    500000,    200000,   2027, 5000,  'medium', 'on_track', 'Char Dham Yatra'),
-- Natasha DSouza (16)
(16, 'Own Flat in Mumbai',             'house',       12000000,  200000,   2033, 15000, 'high',   'behind',   'Andheri or Bandra West'),
(16, 'Retirement Corpus',              'retirement',  20000000,  440000,   2050, 10000, 'high',   'on_track', 'Retire at 60'),
-- Karthik Sundaram (17)
(17, 'FIRE Corpus',                    'retirement',  80000000,  6900000,  2039, 80000, 'high',   'on_track', 'Retire at 50'),
(17, 'Company Equity Exit',            'business',    50000000,  2000000,  2031, 0,     'high',   'ahead',    'Exit from TechSprint AI'),
(17, 'Child Education Fund',           'education',   8000000,   600000,   2041, 20000, 'high',   'on_track', 'Son Arjun - 4 yrs old'),
-- Rekha Pillai (18)
(18, 'Retirement Corpus',              'retirement',  25000000,  2940000,  2028, 30000, 'high',   'on_track', 'Retire at 58 with PF+MF'),
(18, 'Daughter Abroad Education',      'education',   6000000,   500000,   2032, 15000, 'high',   'on_track', 'Pursuing MBBS abroad'),
-- Mohit Srivastava (19)
(19, 'Emergency Fund',                 'emergency',   228000,    112000,   2027, 5000,  'high',   'on_track', '6 months of expenses'),
(19, 'Flat Down Payment',              'house',       2000000,   50000,    2031, 12000, 'high',   'behind',   'Target Hyderabad flat'),
-- Lalitha Krishnan (20)
(20, 'Gold for Daughter Marriage',     'marriage',    1500000,   200000,   2029, 5000,  'high',   'behind',   'Traditional gold reserve'),
(20, 'Emergency Medical Corpus',       'emergency',   300000,    36000,    2027, 5000,  'high',   'behind',   'Medical emergency fund');

-- ─────────────────────────────────────────────────────────────
-- MUTUAL FUND HOLDINGS (62 rows)
-- ─────────────────────────────────────────────────────────────
INSERT INTO mutual_fund_holdings
  (user_id, fund_name, amc_name, category, folio_number, units, nav, purchase_nav,
   current_value, invested_amount, xirr, expense_ratio, monthly_sip, sip_start_date, benchmark) VALUES
-- Rahul Sharma (1) — 5 funds (aggressive)
(1, 'Parag Parikh Flexi Cap Fund - Direct Growth',    'PPFAS AMC',            'Flexi Cap',    'PPFAS/101/2022', 502.31,  72.45,  40.20,   36423.97,  20180.47,  18.2, 0.0062, 3000, '2022-01-10', 'Nifty 500 TRI'),
(1, 'Quant Small Cap Fund - Direct Growth',           'Quant AMC',            'Small Cap',    'QSCP/001/2022', 198.75,  218.30, 120.50,  43372.13,  23949.38,  22.5, 0.0064, 2000, '2022-03-15', 'BSE 250 SmallCap Index TRI'),
(1, 'UTI Nifty 50 Index Fund - Direct Growth',        'UTI AMC',              'Index',        'UTI/502/2021',  804.20,  130.20, 88.40,   104706.84, 71091.48,  15.8, 0.0019, 5000, '2021-06-01', 'Nifty 50 TRI'),
(1, 'Axis Long Term Equity Fund - Direct Growth',     'Axis AMC',             'ELSS',         'AXLT/203/2022', 401.80,  78.60,  55.30,   31581.48,  22219.54,  12.4, 0.0070, 2000, '2022-04-01', 'Nifty 500 TRI'),
(1, 'HDFC Mid-Cap Opportunities Fund - Direct Growth','HDFC AMC',             'Mid Cap',      'HDFC/401/2023', 152.45,  154.80, 105.20,  23599.26,  16036.74,  20.1, 0.0088, 2000, '2023-01-12', 'Nifty Midcap 100 TRI'),
-- Priya Mehta (2) — 4 funds (moderate)
(2, 'Mirae Asset Large Cap Fund - Direct Growth',     'Mirae Asset AMC',      'Large Cap',    'MIRA/301/2020', 1201.54, 89.60,  58.20,   107657.87, 69929.63,  15.4, 0.0056, 5000, '2020-08-01', 'Nifty 100 TRI'),
(2, 'SBI Equity Hybrid Fund - Direct Growth',         'SBI AMC',              'Hybrid',       'SBIH/502/2020', 3204.78, 78.20,  54.40,   250453.72, 174340.03, 13.1, 0.0076, 4000, '2020-05-15', 'Nifty 50 Hybrid Composite TRI'),
(2, 'ICICI Prudential Value Discovery Fund - Direct', 'ICICI Prudential AMC', 'Flexi Cap',    'ICIP/601/2021', 850.22,  78.40,  52.10,   66657.26,  44266.46,  14.5, 0.0095, 2000, '2021-02-10', 'Nifty 500 TRI'),
(2, 'Aditya Birla Sun Life Tax Relief 96 - Direct',   'ABSL AMC',             'ELSS',         'ABSL/801/2022', 604.38,  52.30,  38.80,   31609.07,  23449.96,  11.8, 0.0105, 1500, '2022-03-31', 'Nifty 500 TRI'),
-- Amit Patel (3) — 5 funds (moderate, large corpus)
(3, 'HDFC Top 100 Fund - Direct Growth',              'HDFC AMC',             'Large Cap',    'HDFC/102/2018', 8501.22, 102.40, 58.80,   870524.93, 499871.76, 14.2, 0.0097, 15000, '2018-04-01', 'Nifty 100 TRI'),
(3, 'Kotak Emerging Equity Fund - Direct Growth',     'Kotak AMC',            'Mid Cap',      'KOTK/301/2018', 6804.50, 98.60,  54.20,   671003.70, 368803.90, 16.8, 0.0104, 10000, '2018-07-01', 'Nifty Midcap 100 TRI'),
(3, 'Parag Parikh Flexi Cap Fund - Direct Growth',    'PPFAS AMC',            'Flexi Cap',    'PPFA/401/2019', 12004.80,72.45,  36.80,   869747.76, 441776.64, 17.5, 0.0062, 15000, '2019-01-15', 'Nifty 500 TRI'),
(3, 'Nippon India Small Cap Fund - Direct Growth',    'Nippon AMC',           'Small Cap',    'NIPP/501/2020', 4200.30, 148.90, 85.40,   625404.67, 358905.62, 19.6, 0.0073, 10000, '2020-03-01', 'BSE 250 SmallCap Index TRI'),
(3, 'Franklin India Flexi Cap Fund - Direct Growth',  'Franklin Templeton',   'Flexi Cap',    'FRNK/601/2019', 3800.20, 120.80, 72.60,   459064.16, 275894.52, 14.9, 0.0087, 10000, '2019-06-01', 'Nifty 500 TRI'),
-- Anjali Singh (4) — 4 funds
(4, 'Mirae Asset ELSS Tax Saver Fund - Direct',       'Mirae Asset AMC',      'ELSS',         'MRAL/201/2019', 2804.60, 42.50,  26.80,   119195.50, 75163.28,  13.8, 0.0055, 12500, '2019-04-01', 'Nifty 500 TRI'),
(4, 'HDFC Mid-Cap Opportunities Fund - Direct Growth','HDFC AMC',             'Mid Cap',      'HDFC/401/2019', 2102.40, 154.80, 90.20,   325451.52, 189636.48, 15.2, 0.0088, 8000, '2019-10-01', 'Nifty Midcap 100 TRI'),
(4, 'SBI Bluechip Fund - Direct Growth',              'SBI AMC',              'Large Cap',    'SBIB/301/2020', 3504.80, 72.40,  51.20,   253547.52, 179445.76, 12.4, 0.0068, 8000, '2020-01-01', 'Nifty 100 TRI'),
(4, 'UTI Flexi Cap Fund - Direct Growth',             'UTI AMC',              'Flexi Cap',    'UTIF/401/2021', 2001.20, 48.60,  34.40,   97258.32,  68841.28,  14.7, 0.0085, 8000, '2021-06-01', 'Nifty 500 TRI'),
-- Vikram Nair (5) — 5 funds (aggressive, large)
(5, 'Quant Active Fund - Direct Growth',              'Quant AMC',            'Flexi Cap',    'QACT/001/2018', 8504.30, 612.40, 280.50,  5210393.02, 2385465.15, 22.1, 0.0058, 20000, '2018-10-01', 'Nifty 500 TRI'),
(5, 'Nippon India Small Cap Fund - Direct Growth',    'Nippon AMC',           'Small Cap',    'NIPS/101/2019', 5204.80, 148.90, 78.40,   775034.72, 408056.32, 21.3, 0.0073, 15000, '2019-01-01', 'BSE 250 SmallCap Index TRI'),
(5, 'Motilal Oswal Midcap Fund - Direct Growth',      'Motilal Oswal AMC',    'Mid Cap',      'MOTM/201/2020', 4102.40, 88.40,  48.20,   362652.16, 197735.68, 18.4, 0.0072, 15000, '2020-04-01', 'Nifty Midcap 150 TRI'),
(5, 'ICICI Prudential Technology Fund - Direct',      'ICICI Prudential AMC', 'Sectoral',     'ICST/301/2021', 1802.50, 120.50, 72.40,   217201.25, 130501.00, 19.7, 0.0122, 10000, '2021-02-01', 'Nifty IT TRI'),
(5, 'Edelweiss US Technology Equity FoF - Direct',    'Edelweiss AMC',        'International','EDUS/401/2022', 2204.60, 26.40,  20.50,   58201.44,  45194.30,  8.3,  0.0148, 5000, '2022-03-01', 'Russell 1000 Growth TRI'),
-- Ravi Gupta (7) — 4 funds
(7, 'DSP Tax Saver Fund - Direct Growth',             'DSP AMC',              'ELSS',         'DSPT/101/2021', 1204.80, 32.40,  22.60,   39035.52,  27204.48,  12.8, 0.0068, 5000, '2021-04-01', 'Nifty 500 TRI'),
(7, 'Canara Robeco Equity Hybrid Fund - Direct',      'Canara Robeco AMC',    'Hybrid',       'CNRH/201/2021', 2802.40, 98.60,  70.20,   276356.64, 196728.48, 13.2, 0.0055, 7000, '2021-01-15', 'Nifty 50 Hybrid Composite TRI'),
(7, 'Parag Parikh Flexi Cap Fund - Direct Growth',    'PPFAS AMC',            'Flexi Cap',    'PPFA/501/2022', 1502.80, 72.45,  46.80,   108877.66, 70330.64,  15.4, 0.0062, 5000, '2022-07-01', 'Nifty 500 TRI'),
(7, 'Quant Small Cap Fund - Direct Growth',           'Quant AMC',            'Small Cap',    'QSCS/601/2022', 604.50,  218.30, 140.20,  131975.85, 84738.90,  20.8, 0.0064, 3000, '2022-09-01', 'BSE 250 SmallCap Index TRI'),
-- Deepika Rao (8) — 4 funds  
(8, 'Axis Bluechip Fund - Direct Growth',             'Axis AMC',             'Large Cap',    'AXBL/101/2021', 2204.60, 52.40,  38.20,   115521.24, 84215.72,  11.4, 0.0057, 5000, '2021-03-01', 'Nifty 100 TRI'),
(8, 'Mirae Asset Emerging Bluechip Fund - Direct',    'Mirae Asset AMC',      'Large Cap',    'MIEM/201/2021', 804.50,  104.80, 74.60,   84311.60,  59975.70,  13.8, 0.0078, 5000, '2021-06-15', 'Nifty Large Midcap 250 TRI'),
(8, 'Kotak Emerging Equity Fund - Direct Growth',     'Kotak AMC',            'Mid Cap',      'KOTM/301/2022', 1202.40, 98.60,  64.20,   118556.64, 77194.08,  17.2, 0.0104, 5000, '2022-01-01', 'Nifty Midcap 100 TRI'),
(8, 'Nippon India Small Cap Fund - Direct Growth',    'Nippon AMC',           'Small Cap',    'NIPS/401/2022', 804.20,  148.90, 95.40,   119745.38, 76720.68,  21.9, 0.0073, 5000, '2022-04-01', 'BSE 250 SmallCap Index TRI'),
-- Kavita Joshi (10) — 3 funds
(10, 'SBI Equity Hybrid Fund - Direct Growth',        'SBI AMC',              'Hybrid',       'SBIH/503/2020', 1804.60, 78.20,  56.80,   141239.72, 102501.28, 11.4, 0.0076, 4000, '2020-09-01', 'Nifty 50 Hybrid Composite TRI'),
(10, 'HDFC Top 100 Fund - Direct Growth',             'HDFC AMC',             'Large Cap',    'HDFT/603/2021', 1202.50, 102.40, 76.20,   123136.00, 91630.50,  12.1, 0.0097, 4000, '2021-01-01', 'Nifty 100 TRI'),
(10, 'Axis Long Term Equity Fund - Direct Growth',    'Axis AMC',             'ELSS',         'AXLT/703/2022', 804.30,  78.60,  58.80,   63218.00,  47292.84,  10.7, 0.0070, 2000, '2022-04-01', 'Nifty 500 TRI'),
-- Meera Iyer (12) — 5 funds (aggressive)
(12, 'Quant Active Fund - Direct Growth',             'Quant AMC',            'Flexi Cap',    'QACT/002/2021', 2804.30, 612.40, 320.50,  1716951.72, 898578.65, 23.5, 0.0058, 15000, '2021-01-01', 'Nifty 500 TRI'),
(12, 'Motilal Oswal Midcap Fund - Direct Growth',     'Motilal Oswal AMC',    'Mid Cap',      'MOTM/202/2021', 2402.80, 88.40,  52.20,   212407.52, 125426.16, 20.2, 0.0072, 10000, '2021-04-01', 'Nifty Midcap 150 TRI'),
(12, 'Nippon India Small Cap Fund - Direct Growth',   'Nippon AMC',           'Small Cap',    'NIPS/402/2022', 1204.50, 148.90, 92.40,   179350.05, 111295.80, 22.8, 0.0073, 10000, '2022-01-15', 'BSE 250 SmallCap Index TRI'),
(12, 'Parag Parikh Flexi Cap Fund - Direct Growth',   'PPFAS AMC',            'Flexi Cap',    'PPFA/502/2022', 2004.60, 72.45,  48.20,   145133.17, 96621.72,  16.8, 0.0062, 10000, '2022-07-01', 'Nifty 500 TRI'),
(12, 'UTI Nifty 50 Index Fund - Direct Growth',       'UTI AMC',              'Index',        'UTI/502/2022',  3204.80, 130.20, 98.40,   417145.00, 315352.32, 12.6, 0.0019, 10000, '2022-03-01', 'Nifty 50 TRI'),
-- Karthik Sundaram (17) — 5 funds (aggressive, large)
(17, 'Quant Small Cap Fund - Direct Growth',          'Quant AMC',            'Small Cap',    'QSCK/001/2020', 6804.50, 218.30, 98.60,   1485122.35, 670923.70, 26.4, 0.0064, 25000, '2020-01-01', 'BSE 250 SmallCap Index TRI'),
(17, 'Parag Parikh Flexi Cap Fund - Direct Growth',   'PPFAS AMC',            'Flexi Cap',    'PPFK/201/2020', 8204.80, 72.45,  38.20,   594227.76, 313543.36, 19.8, 0.0062, 20000, '2020-04-01', 'Nifty 500 TRI'),
(17, 'Motilal Oswal Nasdaq 100 FoF - Direct',         'Motilal Oswal AMC',    'International','MOTN/301/2021', 4202.40, 48.20,  28.40,   202515.68, 119348.16, 21.5, 0.0158, 10000, '2021-01-01', 'Nasdaq 100 TRI'),
(17, 'HDFC Mid-Cap Opportunities Fund - Direct Growth','HDFC AMC',            'Mid Cap',      'HDFM/401/2021', 5204.60, 154.80, 86.40,   805672.08, 449677.44, 18.6, 0.0088, 15000, '2021-06-01', 'Nifty Midcap 100 TRI'),
(17, 'Kotak Emerging Equity Fund - Direct Growth',    'Kotak AMC',            'Mid Cap',      'KOTK/501/2022', 3802.40, 98.60,  62.80,   374836.64, 238790.72, 20.1, 0.0104, 10000, '2022-03-01', 'Nifty Midcap 100 TRI'),
-- Rekha Pillai (18) — 3 funds (moderate)
(18, 'HDFC Balanced Advantage Fund - Direct Growth',  'HDFC AMC',             'Hybrid',       'HDFB/101/2019', 5804.60, 82.40,  52.60,   478299.04, 305321.96, 12.2, 0.0082, 10000, '2019-08-01', 'Nifty 50 Hybrid Composite TRI'),
(18, 'SBI Bluechip Fund - Direct Growth',             'SBI AMC',              'Large Cap',    'SBIB/201/2020', 3204.80, 72.40,  52.80,   231947.52, 169213.44, 11.8, 0.0068, 8000, '2020-02-01', 'Nifty 100 TRI'),
(18, 'Axis Long Term Equity Fund - Direct Growth',    'Axis AMC',             'ELSS',         'AXLT/301/2021', 1204.60, 78.60,  58.80,   94681.56,  70830.48,  10.8, 0.0070, 2000, '2021-04-01', 'Nifty 500 TRI'),
-- Sanjay Khanna (15) — 4 funds (conservative/moderate)
(15, 'HDFC Balanced Advantage Fund - Direct Growth',  'HDFC AMC',             'Hybrid',       'HDFB/101/2015', 18204.80,82.40,  26.40,   1500075.52, 480606.72, 12.8, 0.0082, 0, '2015-04-01', 'Nifty 50 Hybrid Composite TRI'),
(15, 'SBI Conservative Hybrid Fund - Direct Growth',  'SBI AMC',              'Hybrid',       'SBIC/201/2016', 12804.60,28.20,  14.80,   361089.72, 189508.08, 11.2, 0.0058, 0, '2016-01-01', 'Nifty 50 Hybrid Composite TRI'),
(15, 'UTI Nifty 50 Index Fund - Direct Growth',       'UTI AMC',              'Index',        'UTIN/301/2017', 6204.80, 130.20, 64.40,   808024.96, 399468.72, 13.8, 0.0019, 0, '2017-06-01', 'Nifty 50 TRI'),
(15, 'ICICI Prudential Debt Fund - Direct Growth',    'ICICI Prudential AMC', 'Debt',         'ICID/401/2018', 48204.80,8.60,   6.20,    414561.28, 298869.76, 7.2,  0.0035, 0, '2018-03-01', 'CRISIL Composite Bond TRI'),
-- Arjun Mehta (21) — 3 funds
(21, 'Axis Bluechip Fund - Direct Growth',            'Axis AMC',             'Large Cap',    'AXBL/102/2020', 3804.60, 52.40,  36.80,   199361.44, 140009.28, 12.2, 0.0057, 8000, '2020-07-01', 'Nifty 100 TRI'),
(21, 'Mirae Asset Large Cap Fund - Direct Growth',    'Mirae Asset AMC',      'Large Cap',    'MIRA/302/2021', 2504.80, 89.60,  66.40,   224430.08, 166318.72, 12.8, 0.0056, 7000, '2021-01-01', 'Nifty 100 TRI'),
(21, 'HDFC Mid-Cap Opportunities Fund - Direct Growth','HDFC AMC',            'Mid Cap',      'HDFC/402/2022', 1802.40, 154.80, 102.40,  278931.52, 184565.76, 16.4, 0.0088, 5000, '2022-06-01', 'Nifty Midcap 100 TRI'),
-- Dr Rohan Singh (23) — 4 funds (aggressive)
(23, 'Quant Active Fund - Direct Growth',             'Quant AMC',            'Flexi Cap',    'QACT/003/2019', 4804.30, 612.40, 240.50,  2943842.92, 1155433.85, 25.6, 0.0058, 25000, '2019-04-01', 'Nifty 500 TRI'),
(23, 'Nippon India Small Cap Fund - Direct Growth',   'Nippon AMC',           'Small Cap',    'NIPS/403/2020', 3204.80, 148.90, 88.40,   477174.72, 283304.32, 23.2, 0.0073, 15000, '2020-01-01', 'BSE 250 SmallCap Index TRI'),
(23, 'Kotak Emerging Equity Fund - Direct Growth',    'Kotak AMC',            'Mid Cap',      'KOTK/503/2020', 3802.40, 98.60,  58.40,   374896.64, 221900.16, 20.8, 0.0104, 15000, '2020-06-01', 'Nifty Midcap 100 TRI'),
(23, 'Parag Parikh Flexi Cap Fund - Direct Growth',   'PPFAS AMC',            'Flexi Cap',    'PPFA/603/2021', 4804.60, 72.45,  46.50,   348093.17, 223413.90, 17.8, 0.0062, 15000, '2021-01-01', 'Nifty 500 TRI');

-- ─────────────────────────────────────────────────────────────
-- TAX PROFILES (20 rows)
-- ─────────────────────────────────────────────────────────────
INSERT INTO tax_profiles
  (user_id, financial_year, gross_salary, hra_received, hra_exemption, lta, section_80c,
   section_80d, section_80d_parents, nps_80ccd, home_loan_interest, section_80g,
   old_regime_tax, new_regime_tax, recommended_regime, tax_saved_if_switched, missed_deductions) VALUES
(1,  '2025-26', 1440000,  240000, 120000, 30000,  150000, 25000,  0,      50000, 0,       0,      117000,  93600,   'new', 23400,  '80G donations, 80CCD NPS employer'),
(2,  '2025-26', 1020000,  264000, 108000, 25000,  140000, 25000,  0,      0,     0,       0,      65520,   66300,   'old', 780,    'NPS 80CCD - can save additional 50k'),
(3,  '2025-26', 3000000,  0,      0,      50000,  150000, 50000,  50000,  50000, 0,       50000,  675000,  721500,  'old', 46500,  'Home loan interest, 80G donations'),
(4,  '2025-26', 2160000,  360000, 144000, 40000,  150000, 25000,  50000,  50000, 0,       25000,  312000,  357000,  'old', 45000,  'HRA optimization, 80G max limit'),
(5,  '2025-26', 3600000,  600000, 240000, 60000,  150000, 25000,  0,      50000, 312000,  0,      702000,  936000,  'old', 234000, 'Home loan interest exemption key benefit'),
(6,  '2025-26', 540000,   180000, 72000,  20000,  120000, 25000,  50000,  0,     0,       0,      0,       3900,    'new', 3900,   'Section 87A rebate applies - zero tax in new'),
(7,  '2025-26', 1140000,  228000, 91200,  25000,  150000, 25000,  0,      50000, 0,       10000,  84240,   63000,   'new', 21240,  '80G donations, home loan interest once bought'),
(8,  '2025-26', 1320000,  264000, 105600, 30000,  100000, 25000,  0,      52000, 0,       0,      118800,  96900,   'new', 21900,  '80C not maxed out, NPS employer contribution'),
(9,  '2025-26', 660000,   0,      0,      15000,  60000,  15000,  50000,  0,     0,       5000,   23400,   17550,   'new', 5850,   '80C underutilised, 80D parents max eligible'),
(10, '2025-26', 840000,   252000, 100800, 20000,  150000, 25000,  0,      0,     0,       0,      42000,   28600,   'new', 13400,  'NPS 80CCD can save additional 50k/year'),
(11, '2025-26', 456000,   0,      0,      10000,  24000,  5000,   0,      0,     0,       0,      0,       0,       'new', 0,      'Below exemption limit in new regime - zero tax'),
(12, '2025-26', 1680000,  336000, 134400, 35000,  150000, 25000,  0,      50000, 0,       20000,  179400,  148500,  'new', 30900,  '80G, home loan interest once purchased'),
(13, '2025-26', 960000,   240000, 96000,  20000,  150000, 25000,  50000,  0,     276000,  10000,  0,       37500,   'old', 37500,  'Home loan interest saves significantly in old regime'),
(14, '2025-26', 504000,   120000, 48000,  10000,  40000,  5000,   0,      0,     0,       0,      0,       0,       'new', 0,      '80C not maximised, NPS 80CCD unexplored'),
(15, '2025-26', 336000,   0,      0,      0,      50000,  25000,  50000,  0,     0,       5000,   0,       0,       'new', 0,      'Pension income - well optimized already'),
(16, '2025-26', 744000,   252000, 100800, 20000,  120000, 25000,  0,      0,     0,       0,      23400,   18200,   'new', 5200,   '80C not maxed, NPS 80CCD can help'),
(17, '2025-26', 2400000,  480000, 192000, 50000,  150000, 25000,  0,      50000, 360000,  0,      444000,  507000,  'old', 63000,  'Home loan interest key - stay old regime'),
(18, '2025-26', 1200000,  300000, 120000, 30000,  150000, 25000,  50000,  50000, 180000,  0,      84000,   81000,   'new', 3000,   'Borderline case - review annually'),
(19, '2025-26', 624000,   156000, 62400,  15000,  93600,  10000,  0,      52000, 0,       0,      0,       4725,    'new', 4725,   '80C not fully utilised, 80D health insurance'),
(20, '2025-26', 180000,   0,      0,      0,      0,      5000,   0,      0,     0,       0,      0,       0,       'new', 0,      'Below basic exemption - no tax payable');

-- ─────────────────────────────────────────────────────────────
-- LIFE EVENTS (28 rows)
-- ─────────────────────────────────────────────────────────────
INSERT INTO life_events (user_id, event_type, event_date, amount_involved, description, ai_recommendation, action_items, status) VALUES
(1,  'bonus',          '2026-03-15', 200000,   'Performance bonus received from Infosys',
     'Invest 50% in PPFAS Flexi Cap (top up SIP), allocate 30% to emergency fund, keep 20% for Europe trip',
     '1. Top up PPFAS SIP by ₹5k/mo. 2. Transfer 60k to emergency savings. 3. Book Europe flights now.', 'recent'),
(1,  'job_change',     '2026-06-01', 1500000,  'Considering offer from Google India for ₹45 LPA CTC',
     'Negotiate joining bonus, check ESOP vesting schedule, update insurance nominees, increase SIP by ₹15,000',
     '1. Calculate PF withdrawal/transfer. 2. Increase 80C investments. 3. Start NPS for extra 50k deduction.', 'upcoming'),
(2,  'baby',           '2024-11-10', 300000,   'Second baby expected - maternity planning required',
     'Maternity corpus ₹3L ready. Start child education SIP of ₹5000 immediately for new child.',
     '1. Open Mirae ELSS in childs name. 2. Add child to health insurance. 3. Review term cover adequacy.', 'recent'),
(2,  'home_purchase',  '2027-01-01', 15000000, 'Planning to buy 2BHK in Thane for ₹1.5 Cr',
     'Down payment 20% = ₹30L needed by Dec 2026. Take ₹1.2Cr home loan at 8.5%. EMI ~₹94k/month.',
     '1. Save ₹25k extra/month for 18 months. 2. Pre-close car loan. 3. Get home loan pre-approval.', 'upcoming'),
(3,  'business_start', '2026-09-01', 20000000, 'New manufacturing unit expansion in Surat',
     'Fund ₹1 Cr from business profits, ₹1 Cr from PF/FD exit, ₹2 Cr via MSME loan at 9%.',
     '1. Structure new entity for tax efficiency. 2. Evaluate MSME loan options. 3. Reduce personal MF SIP temporarily.', 'upcoming'),
(4,  'inheritance',    '2025-12-20', 5000000,  'Received ₹50L inheritance from late father-in-law',
     'Park in SBI Liquid Fund for 3 months. Then split: 40% equity MFs, 30% PPF, 20% gold ETF, 10% FD.',
     '1. Declare inheritance in ITR. 2. Check stamp duty on inherited property. 3. Update will.', 'recent'),
(5,  'home_purchase',  '2023-08-15', 30000000, 'Bought Worli Sea-facing 4BHK apartment for ₹3 Cr',
     'Home loan at ₹1.2 Cr. Maintain old tax regime to claim ₹2L interest deduction. EMI manageable.',
     '1. Claim full ₹2L home loan interest. 2. Claim principal in 80C. 3. Review rent vs own calculation.', 'handled'),
(6,  'marriage',       '2030-05-01', 2000000,  'Elder daughters marriage planned in 2030',
     'Need ₹20L total. Currently have ₹1.2L saved. SIP ₹8k/month in hybrid fund for 4 years = ₹5.2L.',
     '1. Open dedicated SIP for marriage goal. 2. Consider SGB (Sovereign Gold Bond) for gold component.', 'upcoming'),
(7,  'home_purchase',  '2030-06-01', 8000000,  'Planning to buy 3BHK in Hyderabad Madhapur',
     'Down payment ₹20L by 2030. Home loan ₹60L at 8.5%. EMI ₹52k/month. Switch to old regime for interest deduction.',
     '1. Accumulate goal SIP of ₹20k/month. 2. Get home loan pre-approval by 2029. 3. Negotiate builder price.', 'upcoming'),
(8,  'job_change',     '2026-04-01', 1800000,  'Got Senior PM offer from Swiggy at ₹54 LPA',
     'Increased income by ₹8L/year. Increase SIP by ₹20k/month. Target FIRE goal accelerated by 2 years.',
     '1. Update SIP amounts. 2. Check ESOP terms. 3. Increase term insurance by ₹50L.', 'upcoming'),
(9,  'medical_emergency','2025-09-10',150000,  'Wife hospitalized for cardiac surgery',
     'Emergency fund partially used. Rebuild fund immediately. Review health cover - currently under-insured.',
     '1. File health insurance claim. 2. Increase health cover to ₹10L. 3. Add critical illness rider.', 'handled'),
(10, 'baby',           '2026-01-20', 250000,   'Second child delivered - planning education corpus',
     'Start SIP of ₹5,000 in ELSS fund for child. This locks in ₹60k/year in 80C and grows for 18 years.',
     '1. Open Mirae ELSS SIP for new child. 2. Increase health cover to ₹7L. 3. Review term cover.', 'recent'),
(11, 'job_change',     '2026-07-01', 600000,   'Promotion opportunity in Asian Paints regional manager role',
     'Income increase ~₹15k/month. Begin SIP investment from salary hike. Start 80C investments.',
     '1. Start ₹5k SIP in UTI Nifty 50 Index. 2. Buy ₹25L term plan. 3. Open PPF account.', 'upcoming'),
(12, 'job_change',     '2026-05-01', 2400000,  'Received FAANG offer from Amazon at ₹72 LPA',
     'Income jump from ₹1.4L to ₹2L/month. Increase SIP by ₹30k. Accelerate FIRE target by 3 years.',
     '1. Max out NPS (50k extra deduction). 2. Explore US equity international funds. 3. Review FIRE number.', 'upcoming'),
(13, 'home_purchase',  '2020-06-15', 8000000,  'Purchased 3BHK villa in Kakkanad at ₹80L',
     'Home loan ₹60L at 8.2%. 20-year tenure. Currently in old regime - optimal for home loan benefit.',
     '1. Claim ₹2L interest annually. 2. Consider part-prepayment from bonus. 3. Review in 5 years.', 'handled'),
(15, 'retirement',     '2023-01-01', 0,        'Retired from IAS service after 32 years',
     'Pension ₹28k/month secured. PF of ₹50L accumulated. Focus on capital preservation and income.',
     '1. Move PF to SCSS (Senior Citizen Savings Scheme). 2. Set up SWP from MF for top-up income.', 'handled'),
(16, 'bonus',          '2026-02-01', 120000,   'Annual bonus received at Times of India',
     'Invest ₹60k in ELSS for 80C. ₹30k for emergency fund top-up. ₹30k for Goa vacation.',
     '1. Book ELSS investment before March 31. 2. Compare old vs new regime for this year.', 'recent'),
(17, 'business_start', '2021-03-01', 5000000,  'TechSprint AI raised Seed round of ₹5 Cr',
     'Personal finances separated from business. Keep ₹60L liquid emergency fund. Continue personal SIPs.',
     '1. Maintain personal MF SIPs separately. 2. Buy ₹2Cr term cover. 3. ESOP planning for tax.', 'handled'),
(17, 'baby',           '2022-08-15', 0,        'Son Arjun born in August 2022',
     'Start SIP ₹5k in Parag Parikh Flexi Cap for childs higher education. Target ₹80L by 2040.',
     '1. Open minor folio in PPFAS. 2. Add child to ₹20L health cover. 3. Increase term cover by ₹50L.', 'handled'),
(18, 'home_purchase',  '2018-04-01', 6000000,  'Purchased 3BHK apartment in Trivandrum at ₹60L',
     'Home loan ₹40L at 8.5%. Availing ₹2L interest deduction. Old regime beneficial.',
     '1. Continue home loan interest deduction. 2. Consider foreclosure in 2028 post retirement.', 'handled'),
(19, 'education',      '2026-08-01', 500000,   'Enrolled in online MSc Data Science - ₹5L total fees',
     'Split payment over 2 years. Claim 80E education loan interest if taking loan. Upskill for higher salary.',
     '1. Explore education loan for 80E benefit. 2. Negotiate salary hike post-certification.', 'upcoming'),
(20, 'medical_emergency','2025-08-20',80000,   'Husband hospitalized for knee surgery',
     'Emergency fund depleted. Health insurance covered ₹50k. Remaining ₹30k from savings.',
     '1. Rebuild emergency fund of ₹3L. 2. Upgrade health cover to ₹5L. 3. Add critical illness clause.', 'handled'),
(21, 'marriage',       '2023-11-25', 1500000,  'Wedding with Priya Mehta - joint financial planning started',
     'Combine financial planning. Priya claims HRA. Arjun contributes to home down-payment corpus.',
     '1. Open joint goals tracking. 2. Review combined insurance coverage. 3. Joint will planning.', 'handled'),
(23, 'home_purchase',  '2021-05-01', 25000000, 'Purchased 4BHK in South Delhi for ₹2.5 Cr',
     'Home loan ₹80L at 8.4%. Old tax regime saves ₹1.5L tax on home loan interest annually.',
     '1. Maintain old tax regime. 2. Joint ownership with wife for stamp duty saving. 3. Review in 2026.', 'handled');

-- ─────────────────────────────────────────────────────────────
-- INSURANCE POLICIES (42 rows)
-- ─────────────────────────────────────────────────────────────
INSERT INTO insurance_policies
  (user_id, policy_type, insurer_name, policy_number, sum_assured, annual_premium, cover_start_date, cover_end_date, is_active) VALUES
(1,  'term_life',       'HDFC Life',          'HDFC-TRM-2022-00101', 10000000,  12800,  '2022-01-15', '2052-01-15', true),
(1,  'health',          'Star Health',         'STAR-HLT-2022-00201', 500000,    14200,  '2022-02-01', '2027-02-01', true),
(2,  'term_life',       'ICICI Prudential',   'ICIC-TRM-2020-00301', 5000000,   9500,   '2020-08-01', '2055-08-01', true),
(2,  'health',          'Care Health',         'CARE-HLT-2021-00401', 300000,    8800,   '2021-01-01', '2026-01-01', true),
(3,  'term_life',       'LIC India',          'LIC-TRM-2018-00501',  25000000,  28500,  '2018-04-01', '2038-04-01', true),
(3,  'health',          'HDFC ERGO',          'HDFE-HLT-2019-00601', 1000000,   32000,  '2019-01-01', '2027-01-01', true),
(3,  'vehicle',         'Bajaj Allianz',      'BAJA-VEH-2024-00701', 0,         18500,  '2024-06-01', '2025-06-01', false),
(4,  'term_life',       'Max Life',           'MAXL-TRM-2019-00801', 20000000,  22400,  '2019-10-01', '2056-10-01', true),
(4,  'health',          'Star Health',         'STAR-HLT-2020-00901', 1000000,   28600,  '2020-01-01', '2027-01-01', true),
(4,  'critical_illness','HDFC Life',          'HDFC-CRT-2021-01001', 5000000,   18200,  '2021-04-01', '2036-04-01', true),
(5,  'term_life',       'Max Life',           'MAXL-TRM-2018-01101', 30000000,  36800,  '2018-10-01', '2053-10-01', true),
(5,  'health',          'Care Health',         'CARE-HLT-2019-01201', 2000000,   48000,  '2019-03-01', '2027-03-01', true),
(5,  'critical_illness','ICICI Prudential',   'ICIC-CRT-2020-01301', 5000000,   22600,  '2020-01-01', '2040-01-01', true),
(6,  'term_life',       'LIC India',          'LIC-TRM-2015-01401',  3000000,   8400,   '2015-06-01', '2038-06-01', true),
(6,  'health',          'Star Health',         'STAR-HLT-2018-01501', 300000,    9600,   '2018-04-01', '2026-04-01', true),
(7,  'term_life',       'HDFC Life',          'HDFC-TRM-2021-01601', 10000000,  13600,  '2021-03-01', '2056-03-01', true),
(7,  'health',          'Care Health',         'CARE-HLT-2021-01701', 500000,    12800,  '2021-04-01', '2026-04-01', true),
(8,  'term_life',       'Max Life',           'MAXL-TRM-2021-01801', 5000000,   9200,   '2021-08-01', '2056-08-01', true),
(8,  'health',          'Niva Bupa',          'NIVA-HLT-2022-01901', 300000,    10400,  '2022-01-01', '2027-01-01', true),
(9,  'term_life',       'LIC India',          'LIC-TRM-2014-02001',  2000000,   18200,  '2014-08-01', '2032-08-01', true),
(9,  'health',          'Star Health',         'STAR-HLT-2016-02101', 200000,    12400,  '2016-04-01', '2026-04-01', true),
(10, 'term_life',       'HDFC Life',          'HDFC-TRM-2020-02201', 5000000,   11200,  '2020-05-01', '2052-05-01', true),
(10, 'health',          'Care Health',         'CARE-HLT-2020-02301', 300000,    10800,  '2020-06-01', '2026-06-01', true),
(11, 'term_life',       'LIC India',          'LIC-TRM-2023-02401',  2000000,   6800,   '2023-01-01', '2058-01-01', true),
(12, 'term_life',       'ICICI Prudential',   'ICIC-TRM-2021-02501', 10000000,  12400,  '2021-07-01', '2056-07-01', true),
(12, 'health',          'Niva Bupa',          'NIVA-HLT-2022-02601', 500000,    13200,  '2022-01-01', '2027-01-01', true),
(13, 'term_life',       'LIC India',          'LIC-TRM-2016-02701',  8000000,   22800,  '2016-06-01', '2041-06-01', true),
(13, 'health',          'Star Health',         'STAR-HLT-2017-02801', 500000,    18400,  '2017-04-01', '2027-04-01', true),
(14, 'term_life',       'LIC India',          'LIC-TRM-2024-02901',  2000000,   5600,   '2024-01-01', '2059-01-01', true),
(15, 'term_life',       'LIC India',          'LIC-TRM-2005-03001',  10000000,  48000,  '2005-04-01', '2028-04-01', true),
(15, 'health',          'Star Health',         'STAR-HLT-2015-03101', 500000,    22400,  '2015-04-01', '2026-04-01', true),
(16, 'term_life',       'Max Life',           'MAXL-TRM-2020-03201', 5000000,   9600,   '2020-09-01', '2055-09-01', true),
(17, 'term_life',       'HDFC Life',          'HDFC-TRM-2021-03301', 20000000,  24800,  '2021-10-01', '2051-10-01', true),
(17, 'health',          'Care Health',         'CARE-HLT-2022-03401', 2000000,   42000,  '2022-01-01', '2027-01-01', true),
(18, 'term_life',       'LIC India',          'LIC-TRM-2015-03501',  10000000,  32000,  '2015-08-01', '2038-08-01', true),
(18, 'health',          'Star Health',         'STAR-HLT-2016-03601', 1000000,   26400,  '2016-04-01', '2027-04-01', true),
(19, 'term_life',       'HDFC Life',          'HDFC-TRM-2024-03701', 3000000,   7200,   '2024-03-01', '2059-03-01', true),
(20, 'term_life',       'LIC India',          'LIC-TRM-2012-03801',  2000000,   14400,  '2012-06-01', '2032-06-01', true),
(21, 'term_life',       'Max Life',           'MAXL-TRM-2020-03901', 15000000,  20400,  '2020-11-01', '2055-11-01', true),
(21, 'health',          'Niva Bupa',          'NIVA-HLT-2021-04001', 1000000,   22800,  '2021-01-01', '2027-01-01', true),
(23, 'term_life',       'ICICI Prudential',   'ICIC-TRM-2018-04101', 40000000,  44000,  '2018-05-01', '2048-05-01', true),
(23, 'health',          'Care Health',         'CARE-HLT-2019-04201', 2000000,   54000,  '2019-01-01', '2027-01-01', true);

-- ─────────────────────────────────────────────────────────────
-- COUPLE PROFILES (5 rows)
-- ─────────────────────────────────────────────────────────────
INSERT INTO couple_profiles
  (partner1_user_id, partner2_user_id, combined_monthly_income, combined_monthly_expenses,
   combined_net_worth, joint_hra_savings, recommended_nps_split, recommended_sip_split,
   joint_goals, insurance_gaps, optimization_summary) VALUES
(2,  21, 255000, 135000, 4380000, 48000,
  '{"priya_nps_yearly": 50000, "arjun_nps_yearly": 50000, "tax_saving": 26000}',
  '{"priya_total_sip": 22500, "arjun_total_sip": 25000, "allocation": "60% equity, 30% hybrid, 10% debt"}',
  '[{"goal":"Home Purchase Mumbai","target":15000000,"year":2032},{"goal":"Child Education","target":5000000,"year":2040}]',
  'Priya needs health cover upgrade to ₹7L. Arjun needs critical illness ₹50L.',
  'Combined income ₹2.55L. Priya claims full HRA saving ₹48k/year. Arjun contributes ₹25k more to equity SIP. Max NPS for both for extra ₹50k deduction each. Combined tax saving potential ₹1.2L/year.'),

(3,  22, 258000, 137000, 26730000, 0,
  '{"amit_nps_yearly": 50000, "geeta_nps_yearly": 0, "note": "Geeta homemaker - Amit max NPS"}',
  '{"amit_total_sip": 175000, "geeta_total_sip": 5000, "allocation": "50% equity, 30% debt, 20% other"}',
  '[{"goal":"Business Expansion","target":20000000,"year":2028},{"goal":"Children Education","target":10000000,"year":2033}]',
  'Geeta has no term cover - needs ₹1Cr policy. Joint home loan - both should have term cover.',
  'Geeta has income from family business profit sharing. Structure HUF for tax efficiency. Amit to max NPS. Real estate heavy - diversify into financial assets. Reduce gold allocation from 20% to 10%.'),

(4,  23, 580000, 270000, 47440000, 144000,
  '{"anjali_nps_yearly": 50000, "rohan_nps_yearly": 50000, "tax_saving": 52000}',
  '{"anjali_total_sip": 68000, "rohan_total_sip": 120000, "allocation": "70% equity, 20% hybrid, 10% international"}',
  '[{"goal":"Children Education Abroad","target":8000000,"year":2038},{"goal":"Second Home","target":8000000,"year":2030},{"goal":"Combined Retirement","target":120000000,"year":2047}]',
  'Anjali needs critical illness ₹50L rider. Combined health cover ₹40L recommended vs current ₹30L.',
  'Power couple with ₹5.8L combined income. Both max NPS for ₹52k additional saving. Anjali claims full HRA. Home loan interest deduction continues. Children education goal on track with combined SIP. Suggest joint property in both names for mutual tax benefit.'),

(5,  24, 355000, 188000, 36193000, 240000,
  '{"vikram_nps_yearly": 50000, "nisha_nps_yearly": 50000, "tax_saving": 52000}',
  '{"vikram_total_sip": 245000, "nisha_total_sip": 15000, "allocation": "75% equity, 15% international, 10% gold"}',
  '[{"goal":"FIRE Target 55","target":100000000,"year":2046},{"goal":"Child Education","target":10000000,"year":2040}]',
  'Joint health cover needs upgrade to ₹50L (Vikram high income - expensive hospital risk). Nisha needs ₹1Cr additional term cover.',
  'Vikram earns ₹3L + Nisha ₹55k = ₹3.55L combined. Vikram already maximizing investments aggressively. Nisha home studio income - structure as proprietary business for deductions. Joint home loan Worli flat - maintain old regime for interest benefit. ESOP liquidity event expected in 3-4 years.'),

(6,  25, 165000, 102000, 5488000, 0,
  '{"sunita_nps_yearly": 0, "ramesh_nps_yearly": 50000, "note": "Sunita covered by SBI pension"}',
  '{"sunita_total_sip": 19000, "ramesh_total_sip": 10000, "allocation": "40% equity, 40% hybrid, 20% debt"}',
  '[{"goal":"Daughter Marriage","target":2000000,"year":2030},{"goal":"Son Education","target":2500000,"year":2032},{"goal":"Combined Retirement","target":15000000,"year":2035}]',
  'Sunita has government pension but needs additional private health cover. Ramesh term cover adequate.',
  'Sunita has pension income + salary = ₹73k. Ramesh business income ₹92k. Real estate in Jaipur worth ₹80L. Focus on children goals through joint SIP. Daughter marriage fund critical - increase from ₹8k to ₹12k SIP. Ramesh should open NPS for ₹50k additional deduction.');

-- ─────────────────────────────────────────────────────────────
-- MONEY HEALTH SCORES (20 rows)
-- ─────────────────────────────────────────────────────────────
INSERT INTO money_health_scores
  (user_id, overall_score, grade, emergency_preparedness, insurance_coverage,
   investment_diversification, debt_health, tax_efficiency, retirement_readiness,
   strengths, weaknesses, top_recommendations) VALUES
(1,  72.4, 'B', 72.0, 75.0, 80.0, 65.0, 60.0, 68.0,
  'investment_diversification,insurance_coverage',
  'tax_efficiency,debt_health',
  '1. Increase emergency fund to 6 months. 2. Max out NPS for ₹50k extra deduction. 3. Close car loan early.'),
(2,  64.8, 'C', 66.0, 70.0, 68.0, 58.0, 62.0, 60.0,
  'insurance_coverage',
  'debt_health,retirement_readiness',
  '1. Pre-close personal loan. 2. Increase retirement SIP by ₹5k. 3. Upgrade health cover to ₹5L.'),
(3,  78.2, 'B', 78.0, 72.0, 70.0, 62.0, 75.0, 85.0,
  'retirement_readiness,tax_efficiency',
  'investment_diversification',
  '1. Reduce real estate concentration (60% in RE). 2. Increase equity MF allocation. 3. Open separate emergency FD.'),
(4,  82.6, 'A', 85.0, 88.0, 78.0, 88.0, 76.0, 80.0,
  'insurance_coverage,emergency_preparedness,debt_health',
  'tax_efficiency',
  '1. Year-on-year tax regime comparison needed. 2. Explore 80G donations. 3. International fund exposure.'),
(5,  88.4, 'A', 86.0, 90.0, 85.0, 82.0, 78.0, 92.0,
  'retirement_readiness,insurance_coverage,investment_diversification',
  '',
  '1. Consider NPS for ₹50k additional deduction. 2. Review international fund allocation (currently low). 3. Estate planning - will and nominee update.'),
(6,  48.2, 'D', 44.0, 45.0, 38.0, 55.0, 52.0, 52.0,
  'debt_health',
  'investment_diversification,emergency_preparedness,insurance_coverage',
  '1. Increase SIP by ₹2k/month to ₹7k. 2. Upgrade health cover to ₹5L family floater. 3. Start NPS for retirement.'),
(7,  70.8, 'B', 75.0, 72.0, 72.0, 88.0, 65.0, 58.0,
  'debt_health,emergency_preparedness',
  'retirement_readiness',
  '1. Increase retirement SIP by ₹10k. 2. Max NPS 80CCD deduction. 3. Buy home to start home loan interest benefit.'),
(8,  68.4, 'C', 68.0, 62.0, 72.0, 72.0, 62.0, 68.0,
  'investment_diversification',
  'insurance_coverage,tax_efficiency',
  '1. Increase term cover by ₹50L post job change. 2. Max 80C investments. 3. Close personal loan in 6 months.'),
(9,  42.6, 'D', 38.0, 45.0, 35.0, 50.0, 48.0, 48.0,
  'debt_health',
  'investment_diversification,emergency_preparedness,insurance_coverage',
  '1. Increase health cover to ₹5L. 2. Open PPF for ₹500/month. 3. Start ₹2k SIP in balanced fund.'),
(10, 66.4, 'C', 62.0, 68.0, 65.0, 72.0, 60.0, 62.0,
  'debt_health',
  'emergency_preparedness,retirement_readiness',
  '1. Build emergency fund to ₹3L. 2. Start NPS for ₹50k deduction. 3. Increase retirement SIP by ₹5k.'),
(11, 32.8, 'F', 35.0, 25.0, 22.0, 42.0, 48.0, 28.0,
  '',
  'insurance_coverage,investment_diversification,retirement_readiness',
  '1. Buy ₹25L term plan immediately (₹68/month at age 27). 2. Buy ₹5L health cover. 3. Start ₹1k SIP.'),
(12, 80.2, 'A', 82.0, 78.0, 88.0, 90.0, 70.0, 75.0,
  'debt_health,investment_diversification',
  'tax_efficiency',
  '1. Max NPS for additional deduction. 2. Add international equity exposure. 3. Start home purchase goal.'),
(13, 62.8, 'C', 58.0, 68.0, 62.0, 52.0, 68.0, 65.0,
  'tax_efficiency',
  'emergency_preparedness,debt_health',
  '1. Increase emergency fund to ₹3.3L. 2. Prepay home loan ₹1L extra this year. 3. Increase SIP by ₹5k.'),
(14, 44.6, 'D', 42.0, 35.0, 38.0, 52.0, 42.0, 48.0,
  'debt_health',
  'insurance_coverage,investment_diversification',
  '1. Buy ₹25L term cover. 2. Max 80C investments. 3. Repay personal loan in next 12 months.'),
(15, 76.4, 'B', 88.0, 75.0, 72.0, 90.0, 78.0, 88.0,
  'debt_health,retirement_readiness,emergency_preparedness',
  '',
  '1. Move PF to SCSS for 8.2% return. 2. Set up SWP from MF portfolio. 3. Update will and nominees.'),
(16, 58.2, 'C', 58.0, 55.0, 58.0, 62.0, 52.0, 58.0,
  '',
  'insurance_coverage,tax_efficiency',
  '1. Max 80C investments. 2. Upgrade health cover to ₹5L. 3. Add NPS for ₹50k deduction.'),
(17, 84.6, 'A', 86.0, 82.0, 88.0, 78.0, 78.0, 88.0,
  'investment_diversification,retirement_readiness',
  '',
  '1. Add pure debt allocation (currently all equity). 2. Estate planning given high net worth. 3. Consider index funds for 20% of corpus.'),
(18, 74.8, 'B', 77.0, 78.0, 70.0, 72.0, 68.0, 78.0,
  'insurance_coverage,retirement_readiness',
  '',
  '1. Prepay home loan from 2026 bonus. 2. Review hybrid fund allocation as retirement nears. 3. Move some FD to SGB.'),
(19, 52.4, 'C', 55.0, 45.0, 48.0, 55.0, 52.0, 58.0,
  '',
  'insurance_coverage,investment_diversification',
  '1. Upgrade health cover from ₹2L to ₹5L. 2. Increase SIP to ₹5k. 3. Max 80C this year.'),
(20, 40.2, 'D', 42.0, 38.0, 35.0, 88.0, 38.0, 40.0,
  'debt_health',
  'insurance_coverage,investment_diversification,emergency_preparedness',
  '1. Rebuild emergency fund ₹3L. 2. Start ₹1k SIP in balanced hybrid. 3. Upgrade health cover to ₹5L.');
