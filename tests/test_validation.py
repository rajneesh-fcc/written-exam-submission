import pandas as pd

# Check required columns exist in dim_user
def test_dim_user_required_columns():
    df = pd.read_csv('output/dim_user.csv')
    required_cols = ['user_id', 'username', 'email_x']
    for col in required_cols:
        assert col in df.columns, f"Missing required column {col} in dim_user"

# Ensure user_id is unique in dim_user
def test_dim_user_unique_user_id():
    df = pd.read_csv('output/dim_user.csv')
    assert df['user_id'].is_unique, "user_id values are not unique in dim_user"

# Check required columns exist in fact_user_plan
def test_fact_user_plan_required_columns():
    df = pd.read_csv('output/fact_user_plan.csv')
    required_cols = ['user_registration_id', 'plan_id', 'cost_amount']
    for col in required_cols:
        assert col in df.columns, f"Missing required column {col} in fact_user_plan"

# Ensure payment_amount is non-negative in fact_user_plan
def test_fact_user_plan_non_negative_payment():
    df = pd.read_csv('output/fact_user_plan.csv')
    assert (df['cost_amount'] >= 0).all(), "Negative payment_amount found in fact_user_plan"

# Verify foreign key integrity: user_ids in fact_play_session exist in dim_user
def test_fact_play_session_user_id_fk():
    fact_df = pd.read_csv('output/fact_play_session.csv')
    dim_df = pd.read_csv('output/dim_user.csv')
    dim_user_ids = set(dim_df['user_id'])
    invalid_users = fact_df[~fact_df['user_id'].isin(dim_user_ids)]
    assert invalid_users.empty, "fact_play_session contains user_id(s) not in dim_user"
