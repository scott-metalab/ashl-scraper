import requests
import json
from ics import Calendar, Event
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo 


# Step 1: Scrape the schedule
headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': 'Bearer v2.local.RG03ofIgGoreHJq3WpLLbdGINA2oU8XhJdy9yzxUQe2OY1Xfy224Fk0qvRmxSTJwnDzrL95XUZFTw-QWG4w2xfqO71ELYughyRg1lJTWrv8TcKaLMCq4GWpT-zRGaEbHELUEFydi_YfBzW0Y2Dj3D1A-w1qS8n4lyaYMR9qvG1r2_h-EiyFTptxrYVyarSceaUpaOMghK0VwmNu_TNz1wYuqFJKm5iWcPPKyAFCeplbKjAcd9gDxJJZ7mUAInFtuYm5SMksWHDk4xG4TQj0-Fg_kudbVX5Xg0kJ557_jMlzE5GfWocdJRyx7bn5QVoclhAhO1tWb07b_vovqa6Qqby0_qI8',
    'content-type': 'application/json',
    'origin': 'https://www.ashl.ca',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
}

params = {
    'exclude_cancelled_games': '1',
    'team_id': 'pFCCVxgBN9oPfj9i',
    'order': 'asc',
}

response = requests.get(
    'https://canlan2-api.sportninja.net/v1/schedules/tUnpD3Noto6zKNBz/games',
    params=params,
    headers=headers,
)

data = response.json()
print(data)

# with open('testdata.json', 'r') as f:
#     data = json.load(f)

# -- Step 2: Create Calendar --

calendar = Calendar()

# Create calendar event objects
for item in data['data']:  
    home_team = item.get('homeTeam').get('name')
    visitingTeam = item.get('visitingTeam').get('name')
    starts_at = item.get('starts_at')
    ends_at = item.get('ends_at')
    rink = item.get('facility').get('name')

    # Create datetime object, and convert to Pacific Time (handles DST automatically)
    dt_utc = datetime.fromisoformat(starts_at)
    starts_at_pacific = dt_utc.astimezone(ZoneInfo("America/Los_Angeles"))

    # Get opponents name by checking the home and away teams
    if home_team == "Blood Sweat & Beers":
        opponent = visitingTeam
    else:
        opponent = home_team

    event = Event()
    event.name = f"Hockey vs {opponent} [{rink}]"
    event.begin = starts_at_pacific
    event.duration = timedelta(hours=2)
    event.location = "Scotia Barn by Canlan Sports 6501 Sprott St, Burnaby, BC V5B 3B8"

    calendar.events.add(event)

# # -- Step 3: Write .ics File --

with open("hockey_schedule.ics", "w") as f:
    f.writelines(calendar)

print("✅ ICS file generated: hockey_schedule.ics")