import json
import os

SAVE_FILE = "save_data.json"

def load_data():
    if not os.path.exists(SAVE_FILE):
        default_data = {"completed_levels": []}
        save_data(default_data)
        return default_data
    
    try:
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {"completed_levels": []}

def save_data(data):
    try:
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def complete_level(level_num):
    data = load_data()
    completed_levels = data.get("completed_levels", [])
    
    if level_num not in completed_levels:
        completed_levels.append(level_num)
        completed_levels.sort()
        save_data({"completed_levels": completed_levels})
        return True
    return False

def is_level_unlocked(level_num):
    data = load_data()
    completed = data.get("completed_levels", [])
    
    if level_num == 1:
        return True
    
    return (level_num - 1) in completed

def reset_progress():
    save_data({"completed_levels": []})

def get_completed_levels():
    data = load_data()
    return data.get("completed_levels", [])