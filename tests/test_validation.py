import pandas as pd

def test_required_columns():
    df = pd.read_csv('data/user_play_session.csv')
    assert 'user_id' in df.columns, "Missing user_id column"
    assert 'channel_code' in df.columns, "Missing channel_code"

def test_datetime_parsing():
    df = pd.read_csv('data/user_play_session.csv', parse_dates=['start_datetime', 'end_datetime'])
    assert pd.api.types.is_datetime64_any_dtype(df['start_datetime']), "start_datetime is not datetime"
