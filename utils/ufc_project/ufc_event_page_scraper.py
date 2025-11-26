# This script will safely scrape fight level details of a given event page from UFC Stats. Provide an event URL and this script should capture the relevant data needed.

# Imports
import requests
from bs4 import BeautifulSoup
import pandas as pd

EVENT_URL = 'http://ufcstats.com/event-details/bd92cf5da5413d2a'

response = requests.get(EVENT_URL)
soup = BeautifulSoup(response.text, 'html.parser')
if len(soup) == 0:
	assert('Failed to retrieve data from the URL provided.')
else:
	print('Data retrieved.')

fights = []
fight_rows = soup.select("tr.b-fight-details__table-row.b-fight-details__table-row__hover.js-fight-details-click")

for row in fight_rows:
    # fighter names
    fighters = row.select("a.b-link.b-link_style_black")
    fighter_red = fighters[0].text.strip()
    fighter_blue = fighters[1].text.strip()

    # links to fighter pages
    fighter_red_url = fighters[0]["href"]
    fighter_blue_url = fighters[1]["href"]

    # grab the weight class from the correct table column (7th td)
    weight_el = row.select_one("td:nth-of-type(7) p.b-fight-details__table-text")
    weight_class = weight_el.get_text(separator=" ", strip=True) if weight_el else ""

    fights.append({
        "fighter_red": fighter_red,
        "fighter_blue": fighter_blue,
        "red_url": fighter_red_url,
        "blue_url": fighter_blue_url,
        "weight_class": weight_class
    })

df = pd.DataFrame(fights)
df

# Export
df.to_csv('data/ufc_323_event_level_data.csv', index = False)



