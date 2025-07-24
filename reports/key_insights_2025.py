import pandas as pd

# ------------------------------
# 1. Load data
# ------------------------------
fact_play_session = pd.read_csv('output/fact_play_session.csv')
fact_user_plan = pd.read_csv('output/fact_user_plan.csv')
dim_plan = pd.read_csv('output/dim_plan.csv')

# ------------------------------
# 2. Clean column names and types
# ------------------------------
fact_play_session.columns = fact_play_session.columns.str.strip()
fact_user_plan.columns = fact_user_plan.columns.str.strip()
dim_plan.columns = dim_plan.columns.str.strip()

# Debug print to verify
print("\ndim_plan columns:", dim_plan.columns.tolist())
print("fact_user_plan columns:", fact_user_plan.columns.tolist())

# Make sure plan_id is aligned
fact_user_plan['plan_id'] = fact_user_plan['plan_id'].astype(str).str.strip()
dim_plan['plan_id'] = dim_plan['plan_id'].astype(str).str.strip()

# ------------------------------
# 3. Insight 1: Play sessions by channel
# ------------------------------
print("\n--- Insight 1: Play Sessions by Channel ---")
play_sessions_by_channel = fact_play_session['channel_code'].value_counts()
print(play_sessions_by_channel)

# ------------------------------
# 4. Insight 2: Registered users by payment type
# ------------------------------
print("\n--- Insight 2: Registered Users by Payment Type ---")

# Confirm that 'payment_frequency_code' exists before merge
if 'payment_frequency_code' not in dim_plan.columns:
    raise KeyError("'payment_frequency_code' not found in dim_plan.csv")

# Merge
user_plan_with_freq = fact_user_plan.merge(
    dim_plan[['plan_id', 'payment_frequency_code']],
    on='plan_id',
    how='left'
)

# Debug: Show merged columns
print("Merged DataFrame columns:", user_plan_with_freq.columns.tolist())

# Handle case where column might still be missing due to merge failure
if 'payment_frequency_code' not in user_plan_with_freq.columns:
    print("⚠️ Merge failed. Using backup approach.")
    users_by_payment_type = pd.Series(dtype=int)
else:
    # Show if any unmatched rows
    missing_freq = user_plan_with_freq['payment_frequency_code'].isna().sum()
    if missing_freq > 0:
        print(f"⚠️ {missing_freq} rows could not be matched with payment_frequency_code.")

    # Count unique users per frequency
    users_by_payment_type = user_plan_with_freq.groupby('payment_frequency_code')['user_id'].nunique()

print(users_by_payment_type)

# ------------------------------
# 5. Insight 3: Gross revenue
# ------------------------------
print("\n--- Insight 3: Gross Revenue Generated ---")
gross_revenue = fact_user_plan['cost_amount'].sum()
print(f"${gross_revenue:,.2f}")
