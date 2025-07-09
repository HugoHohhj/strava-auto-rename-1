import os, requests, datetime

# 刷新 Token
def refresh_token():
    resp = requests.post('https://www.strava.com/oauth/token', data={
        'client_id': os.getenv('STRAVA_CLIENT_ID'),
        'client_secret': os.getenv('STRAVA_CLIENT_SECRET'),
        'grant_type': 'refresh_token',
        'refresh_token': os.getenv('STRAVA_REFRESH_TOKEN'),
    }).json()
    return resp['access_token'], resp.get('refresh_token')

# 重命名最新活动
def rename_latest(access_token):
    r = requests.get('https://www.strava.com/api/v3/athlete/activities', params={'per_page': 1}, headers={'Authorization': f'Bearer {access_token}'})
    act = r.json()[0]
    act_id = act['id']
    start = datetime.datetime.fromisoformat(act['start_date_local'].replace('Z', ''))
    date_str = start.strftime('%Y-%m-%d')
    new_name = f"{date_str} Evening Ride"
    requests.put(f'https://www.strava.com/api/v3/activities/{act_id}', headers={'Authorization': f'Bearer {access_token}'}, data={'name': new_name})
    print("✅ Renamed to", new_name)

if __name__ == "__main__":
    token, new_refresh = refresh_token()
    rename_latest(token)
    if new_refresh:
        print("♻️ New refresh_token:", new_refresh)
