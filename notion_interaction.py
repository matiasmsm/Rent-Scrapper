from notion_client import Client
from dotenv import load_dotenv
import json
import os
import requests


load_dotenv()
# Initialize the Notion client
NOTION_TOKEN = os.getenv('NOTION_SECRET')

# Replace with your database ID
DATABASE_ID = os.getenv('NOTION_PAGE_ID')


headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages"

    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}

    res = requests.post(create_url, headers=headers, json=payload)
    return res

def write_data(data_list):
    for data_dict in data_list:
        for title, entry in data_dict.items():
            if len(entry.keys()) == 0:
                continue
            try:
                new_entry = {
                    "Titulo": {"title": [{"text": {"content": entry.get("Title", "")}}]},
                    "Ubicacion": {"rich_text": [{"text": {"content": entry.get("Zone", "")}}]},
                    "Precio": {"number": entry.get("Price", 0)},
                    "Tamaño": {"number": entry.get("Size", 0)},
                    "Link": {"url": entry.get("Link", None) if entry.get("Link", "") != "" else None},
                    "Puntaje": {"number": entry.get("Puntaje", None)},
                }

                res = create_page(new_entry)

            except Exception as e:
                continue
