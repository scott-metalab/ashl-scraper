import requests
import json
from ics import Calendar, Event
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo 


# Step 1: Scrape the schedule
headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': 'Bearer v2.local.jRU634hC1t7H0t4HqzuR6qqtA2fsvG2qWKvR5DEQRD57Q9Ti0iAp2Mik9kMJihKYvFMFg0y_Lg__VDkrUkiqeW3TSzG_4fO_LUTrJJMej75t3wtETLlUH8xKg9yt1hvEIeZpbd8PbkLoOaBrQy4E_VLz360O2mO4Nd4Dvz28Od1yJukqAZO83UiTxyR-cFN3h1y2W8ZJwXpWPTDOHz3k-AltCYiGoigQSBwoU0mIr73zGnri4rFXD0tvZ7lNt4T9yXLLM5jpAN33lqCXcInJH-N7PViusVjJz-n1k7962Uw8F6_QWRuZdyl-2zXLRwXPXU17-MwQgy98dXATskyZsN-C4TA',
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