import pandas as pd
import os

DATA_DIR = 'data'
OUTPUT_DIR = 'output'

# Load raw CSVs
df_user = pd.read_csv(f"{DATA_DIR}/user.csv")
df_registration = pd.read_csv(f"{DATA_DIR}/user_registration.csv")
df_play_session = pd.read_csv(f"{DATA_DIR}/user_play_session.csv")
df_channel = pd.read_csv(f"{DATA_DIR}/channel_code.csv")
df_status = pd.read_csv(f"{DATA_DIR}/status_code.csv")
df_user_plan = pd.read_csv(f"{DATA_DIR}/user_plan.csv")
df_plan = pd.read_csv(f"{DATA_DIR}/plan.csv")
df_payment = pd.read_csv(f"{DATA_DIR}/user_payment_detail.csv")
df_freq = pd.read_csv(f"{DATA_DIR}/plan_payment_frequency.csv")

# Dim_User
dim_user = df_registration.merge(df_user, on="user_id", how="left")
dim_user.to_csv(f"{OUTPUT_DIR}/dim_user.csv", index=False)

# Fact_Play_Session
fact_play_session = df_play_session \
    .merge(df_channel, left_on='channel_code', right_on='play_session_channel_code', how='left') \
    .merge(df_status, left_on='status_code', right_on='play_session_status_code', how='left')
fact_play_session.to_csv(f"{OUTPUT_DIR}/fact_play_session.csv", index=False)

# Dim_Plan
dim_plan = df_plan.merge(df_freq, on='payment_frequency_code', how='left')
dim_plan.to_csv(f"{OUTPUT_DIR}/dim_plan.csv", index=False)

# Fact_User_Plan (Payment)
fact_user_plan = df_user_plan \
    .merge(df_payment, on='payment_detail_id', how='left') \
    .merge(df_plan, on='plan_id', how='left')
fact_user_plan.to_csv(f"{OUTPUT_DIR}/fact_user_plan.csv", index=False)

# Example Insight
online_sessions = fact_play_session[fact_play_session['english_description_x'] == 'Online']
mobile_sessions = fact_play_session[fact_play_session['english_description_x'] == 'Mobile']
print(f"Online sessions: {len(online_sessions)}")
print(f"Mobile sessions: {len(mobile_sessions)}")
