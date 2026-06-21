import json
import os


DATA_FILE = os.path.expanduser("~/.podcast_studio.json")

STUDIO_TYPES = ["直播间", "录音间", "会议室"]


def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "studios": {},
            "bookings": {},
            "edit_tasks": {},
            "booking_seq": 0,
            "edit_task_seq": 0,
        }
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
