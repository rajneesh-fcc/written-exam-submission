import pandas as pd

# ------------------------------
# 1. Load data (adjust file paths if needed)
# ------------------------------
fact_play_session = pd.read_csv('output/fact_play_session.csv')
fact_user_plan = pd.read_csv('output/fact_user_plan.csv')
dim_plan = pd.read_csv('output/dim_plan.csv')

# ------------------------------
# 2. Clean column names to avoid whitespace issues
# ------------------------------
dim_plan.columns = dim_plan.columns.str.strip()
fact_user_plan.columns = fact_user_plan.columns.str.strip()
fact_play_session.columns = fact_play_session.columns.str.strip()

# ------------------------------
# 3. Play sessions by channel
# ------------------------------
play_sessions_by_channel = fact_play_session['channel_code'].value_counts()
print("Play Sessions by Channel:\n", play_sessions_by_channel)

# ------------------------------
# 4. Registered users by payment type
# Merge fact_user_plan with dim_plan to get payment frequency per user-plan
# ------------------------------
user_plan_with_freq = fact_user_plan.merge(
    dim_plan[['plan_id', 'payment_frequency_code']],
    on='plan_id',
    how='left'
)

# Count distinct users by payment_frequency
users_by_payment_type = user_plan_with_freq.groupby('payment_frequency_code')['user_id'].nunique()
print("\nRegistered Users by Payment Type:\n", users_by_payment_type)

# ------------------------------
# 5. Gross revenue generated
# ------------------------------
gross_revenue = fact_user_plan['cost_amount'].sum()
print(f"\nGross Revenue Generated: ${gross_revenue:,.2f}")
