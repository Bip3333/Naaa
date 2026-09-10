from connection import supabase

# - Settings

def save_settings(user_id,theme,text_size):
    try:
        supabase.table("user_data").upsert({"user_id": user_id,"theme": theme,"text_size": text_size}).execute()
        return True, "Settings saved successfully"

    except Exception as e:
        print("Settings save error:", e)
        return False, "Could not save settings"


def load_settings(user_id):
    try:
        result = (supabase.table("user_data").select("theme, text_size").eq("user_id", user_id).execute())

        if result.data:
            return result.data[0]

        return None

    except Exception as e:
        print("Settings load error:", e)
        return None

# - Checklist

def add_checklist_item(user_id, task):
    try: 
        result = (supabase.table("checklist_items").insert({"user_id": user_id, "task": task, "completed": False}).execute())

        return True, "Task added successfully"

    except Exception as e:
        print("Checklist add error:", e)
        return False, "Could not add task"

def load_checklist_items(user_id):
    try:
        result = (supabase.table("checklist_items").select("id, task, completed, created_at").eq("user_id", user_id).order("created_at").execute())

        return result.data

    except Exception as e:
        print("Could not load checklist", e)
        return []


def update_checklist_item(user_id, item_id, completed):
    try:
        result = (supabase.table("checklist_items").update({"completed": completed, }).eq("id", item_id).eq("user_id", user_id).execute())

        return True, "Task updated successfully"

    except Exception as e:
        print("Checklist update error", e)
        return False, "could not update task"

def delete_checklist_item(user_id, item_id):
    try:
        result = (supabase.table("checklist_items").delete().eq("id", item_id).eq("user_id", user_id).execute())

        return True, "Task deleted successfully"

    except Exception as e:
        print("Checklist delete error", e)
        return False, "could not delete task"

def load_calender_events(user_id, week_start, week_end):
    try:
        result = (supabase.table("calendar_events").select("id, title, date, start_time, end_time, description").eq("user_id", user_id).gte("date", week_start.isoformat()).lte("date", week_end.isoformat()).order("date").order("start_time").execute())
        return result.data

    except Exception as e:
        print("Calendar events load error", e)
        return []
    