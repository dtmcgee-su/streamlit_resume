import requests 
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

def scrape_fighter_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    def clean(text):
        if text:
            return re.sub(r"\s+", " ", text).strip()
        return None

    # Extract name + nickname
    name = clean(soup.select_one("span.b-content__title-highlight").text)
    nickname_elem = soup.select_one("p.b-content__Nickname")
    nickname = clean(nickname_elem.text) if nickname_elem else None

    # Extract all list items (bio + stats)
    items = soup.select("li.b-list__box-list-item")

    data = {}

    for item in items:
        text = item.get_text(" ", strip=True)
        if ":" in text:
            label, value = text.split(":", 1)
            label = label.strip().lower()
            value = clean(value)
            data[label] = value

    fighter_data = {
        "name": name,
        "nickname": nickname,

        # bio
        "height": data.get("height"),
        "weight": data.get("weight"),
        "reach": data.get("reach"),
        "stance": data.get("stance"),
        "dob": data.get("dob"),

        # striking
        "slpm": data.get("slpm"),
        "sapm": data.get("sapm"),
        "str_acc": data.get("str. acc."),
        "str_def": data.get("str. def."),

        # grappling
        "td_avg": data.get("td avg."),
        "td_acc": data.get("td acc."),
        "td_def": data.get("td def."),
        "sub_avg": data.get("sub. avg."),
    }

    # print(fighter_data)
    return fighter_data

matchups_df = pd.read_csv('data/ufc_323_event_level_data.csv')

stats = {}

urls = set(matchups_df['red_url']).union(set(matchups_df['blue_url']))

print(urls)

for url in urls:
    print(f"Scraping: {url}")
    stats[url] = scrape_fighter_details(url)
    time.sleep(1) 
    # break


def map_stats(row, corner, stats_dict):
    url = row[f"{corner}_url"]
    fighter_stats = stats_dict.get(url, {})
    return pd.Series({f"{corner}_{k}": v for k, v in fighter_stats.items()})

df_final = pd.concat([
    matchups_df,
    matchups_df.apply(lambda r: map_stats(r, "red", stats), axis=1),
    matchups_df.apply(lambda r: map_stats(r, "blue", stats), axis=1),
], axis=1)

print(df_final)

df_final.to_csv('data/ufc_323_fighter_stats.csv', index=False)