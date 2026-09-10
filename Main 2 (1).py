import ttkbootstrap as ttk
import tkinter.font as tkfont
from supabase import create_client
import connection
import auth
import data
from datetime import datetime, timedelta



root = ttk.Window()

# - Layout

root.state("zoomed")

# - Header

main = ttk.Frame(root)
main.grid(row=0, column=1, sticky= "nsew")

main.rowconfigure(1,weight=1)
main.columnconfigure(0,weight=1)

header = ttk.Frame(main)
header.grid(row=0,column=0,sticky="ew")

# - Title header

title_frame = ttk.Frame(header)
title_frame.place(relx=0.5,rely=0.5, anchor="center")

user_icon_frame = ttk.Frame(header)
user_icon_frame.pack(side="right",padx=15)

streak_frame = ttk.Frame(header)
streak_frame.pack(side="right",padx=20)

toggle_sidebar_frame = ttk.Frame(header)
toggle_sidebar_frame.pack(side="left")

# - Folder

folder = ttk.Frame(main)
folder.grid(row=1,column=0,sticky="nsew")

folder.rowconfigure(0,weight=1)
folder.columnconfigure(0,weight=1)

# - Root

root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=1)
root.rowconfigure(0,weight=1)

# - Design

style = ttk.Style()

style.configure("Sidebar.TButton", font=("Helvetica", 12))
style.configure("ChangeTheme.TCombobox", selectbackground=root.style.colors.bg,selectforeground=style.lookup("ChangeTheme.TCombobox","foreground"),fieldbackground=root.style.colors.bg)
style.configure("Usericon.TButton", font=(15))
style.configure("User_button.TButton",font=("Helvetica", 12))
style.configure("Message_sign_in.TLabel",font=("bold", 12),foreground="red")
style.configure("Message_login.TLabel",font=("bold", 12),foreground="red")

# - List of all the themes

days = [
    "Mon",
    "Tue",
    "Wed",
    "Thu",
    "Fri",
    "Sat",
    "Sun"
]

light_themes = [
    "bootstrap-light",
    "pydata-light",
    "nord-light",
    "solarized-light",
    "catppuccin-light",
    "gruvbox-light",
    "dracula-light",
    "tokyo-night-light",
    "one-light",
    "everforest-light",
    "vapor-light",
    "minty-light",
    "pulse-light",
    "united-light",
    "sandstone-light"
]

dark_themes = [
    "bootstrap-dark",
    "pydata-dark",
    "nord-dark",
    "solarized-dark",
    "catppuccin-dark",
    "gruvbox-dark",
    "dracula-dark",
    "tokyo-night-dark",
    "one-dark",
    "everforest-dark",
    "vapor-dark",
    "minty-dark",
    "pulse-dark",
    "united-dark",
    "sandstone-dark"
]


theme_map = {}

for theme in light_themes:
    display_name = "🔆 " + theme.removesuffix("-light").replace("-", " ").title()
    theme_map[display_name] = theme

for theme in dark_themes:
    display_name = "🌙 " + theme.removesuffix("-dark").replace("-", " ").title()
    theme_map[display_name] = theme

# - Pages

home = ttk.Frame(folder)
calendar = ttk.Frame(folder)
settings = ttk.Frame(folder)
checklist = ttk.Frame(folder)
current_tasks = ttk.Frame(folder)
help = ttk.Frame(folder)
user_page = ttk.Frame(folder)
user_sign_in_page = ttk.Frame(folder)
user_login_page = ttk.Frame(folder)

for page in (home,calendar,settings,checklist,current_tasks,help,user_page,user_sign_in_page,user_login_page):
    page.grid(row=0,column=0,sticky="nsew")

# - Sidebar

sidebar = ttk.Frame(root)
sidebar.grid(row=0,column=0,sticky="nsew")

for page in range(6):
    sidebar.rowconfigure(page, weight=1)

sidebar.columnconfigure(0, weight=1)

# - Global var

current_user = None
current_week_start = datetime.today().date()
current_week_start -= timedelta(days=current_week_start.weekday())

# - Button functions

def change_week(amount):
    global current_week_start, week_dates

    current_week_start += timedelta(days=amount*7)

    week_dates = [current_week_start + timedelta(days=i) for i in range(7)]

    load_calendar()

def load_calendar():

    for widget in calendar_grid.winfo_children():
        widget.destroy()

    first_day = week_dates[0]
    last_day = week_dates[-1]

    events = []

    if current_user is not None:
        events = data.load_calender_events(current_user.id,first_day,last_day)

    current_week_title.config(text=f"{first_day.strftime('%d %b')} - {last_day.strftime('%d %b %Y')}")   # Gives the title the form '7 Sep - 13 Sep 2026'

    for column, day_date in enumerate(week_dates, start=1):

        day_name = day_date.strftime("%a")
        day_number = day_date.strftime("%d")

        day_label = ttk.Label(calendar_grid,text=f"{day_name}\n{day_number}",font=("Verdana",10,"bold"),anchor="center")
        day_label.grid(row=0,column=column,sticky="ew",padx=2,pady=(5,10))


    for row, hour in enumerate(range(start_hour, end_hour +1),start=1):

        time_text = datetime.strptime(f"{hour}:00","%H:%M").strftime("%I %p").lstrip("0")

        time_label = ttk.Label(calendar_grid,text=time_text,font=("Verdana",9),anchor="ne")
        time_label.grid(row=row,column=0,sticky="ne",padx=(0,8),pady=2)

        for column in range(1,8):

            time_slot = ttk.Frame(calendar_grid,height=slot_height,relief="solid",borderwidth=1)

            time_slot.grid(row=row,column=column,sticky="ew",padx=2,pady=1)

            time_slot.grid_propagate(False)

    print("Calendar events:", events)

    for event in events:
        print(event)
        event_date = datetime.strptime(event["date"],"%Y-%m-%d").date()

    test_event = ttk.Label(calendar_grid,text="Math",font=("Verdana",10,"bold"))   # This is a fake event to see if the calendar correctly shows the event, it should show maths being at 4PM on a thursday
    test_event.grid(row=9,column=4,sticky="nsew",padx=4,pady=4)

def delete_checklist_item(item_id):
    if current_user is None:
        return

    success, message = data.delete_checklist_item(current_user.id,item_id)

    if not success:
        checklist_message.config(text=message)
        return

    load_checklist()

def toggle_checklist_item(item_id,completed):
    if current_user is None:
        return

    success, message = data.update_checklist_item(current_user.id,item_id,completed)

    if not success:
        checklist_message.config(text=message)
        return

    load_checklist()

def load_checklist():
    for widget in checklist_items_frame.winfo_children():
        widget.destroy()

    if current_user is None:
        return

    items = data.load_checklist_items(current_user.id)

    for index, item in enumerate(items):
        task_frame = ttk.Frame(checklist_items_frame)

        column = index // 12
        row = index % 12   # - Makes the tasks to be formatted in rows and columns

        task_frame.grid(row=row,column=column,padx=20,pady=5,sticky="w")

        completed = item["completed"]

        task_text = item["task"]

        if completed:
            task_text = "✓ " + task_text
        else:
            task_text = "☐ " + task_text

        task_button = ttk.Button(task_frame,text=task_text,command=lambda item_id=item["id"], completed=completed: toggle_checklist_item(item_id, not completed),style="User_button.TButton")
        task_button.pack(side="left")
        task_button.configure(style="User_button.TButton")

        delete_button = ttk.Button(task_frame,text="Delete",command= lambda item_id=item["id"]: delete_checklist_item(item_id))
        delete_button.pack(side="left",padx=5)

def add_checklist_task():
    if current_user is None:
        checklist_message.config(text="Please login to use the checklist")
        return 

    task = checklist_box.get().strip()

    if task == "":
        checklist_message.config(text="Please enter a task ")
        return 

    success, message = data.add_checklist_item(current_user.id,task)

    checklist_message.config(text=message)

    if success:
        checklist_box.delete(0, "end")
        checklist_message.config(text="")
        load_checklist()


def show_streak():
    streak_frame.pack(side="right",padx=20)

def hide_streak():
    streak_frame.pack_forget()

def reset_ui():
    style.theme_use("bootstrap-light")

    theme_drop.set("🔆 Bootstrap")

    text_size.delete(0, "end")
    text_size.insert(0, "12")

    User_profile.config(text="👤")

    change_text_size()

def logout():
    global current_user

    current_user = None

    hide_streak()

    reset_ui()

    show_login_content()

    load_checklist()

    message_login_text.config(text="")

    show_page(user_page,"User")

def hide_login_content():
    user_text_frame.pack_forget()
    user_button_frame.pack_forget()
    guest_frame.pack_forget()
    logout_frame.pack(pady=50)

def show_login_content():
    user_text_frame.pack(pady=100)
    user_button_frame.pack()
    guest_frame.pack()
    logout_frame.pack_forget()


def close_app():
    if current_user:
        selected = theme_drop.get()
        theme_name = theme_map[selected]

        try:
            size = int(text_size.get())

            if 1 <= size <= 20:
                data.save_settings(current_user.id,theme_name,size)

        except ValueError:
            pass

    root.destroy()


def sign_up_button():
    username = username_sign_in_box.get() #Fetches the current username and password in the boxes
    password = password_sign_in_box.get()

    success, message = auth.sign_up(username,password) #goes to auth.py to process this information
    message_sign_in_text.config(text=message) 

def login_button():

    global current_user 

    username = username_login_box.get() 
    password = password_login_box.get() #Fetches the username and password filled in the boxes

    success, message, user = auth.Login(username,password) #processes this information in auth.py

    message_login_text.config(text=message) 

    if success:

        current_user = user  

        show_streak()

        hide_login_content() #Hides the sign in or login option in the user page

        load_checklist()

        username = user.user_metadata.get("username")
        
        User_profile.config(text="👤 " + username.capitalize())

        

        print("Logged in:", current_user.id)

        saved_settings = data.load_settings(current_user.id)

        if saved_settings:

            print("Saved settings", saved_settings) #loads the most recent saved settings in specialised for each user

            saved_theme = saved_settings.get("theme")

            if saved_theme:
                style.theme_use(saved_theme)

                for name, theme_name in theme_map.items():
                    if theme_name == saved_theme:
                        theme_drop.set(name)
                        break

            saved_text_size = saved_settings.get("text_size")

            if saved_text_size:
                text_size.delete(0, "end")
                text_size.insert(0 , str(saved_text_size))
                change_text_size()

        show_page(home, "routineR")


def change_text_size(event=None):
    try:
        Sidebar_size = int(text_size.get())
        if 1 <= Sidebar_size <= 20:
            style.configure("Sidebar.TButton",font=("Helvetica",Sidebar_size))
        
    except ValueError:
        pass

def toggle_fullscreen(event):
    fullscreen = root.attributes("-fullscreen")
    root.attributes("-fullscreen", not fullscreen) 

def change_theme(event):
    selected = theme_drop.get()
    style.theme_use(theme_map[selected])
    style.configure("ChangeTheme.TCombobox", selectbackground=root.style.colors.bg,selectforeground=style.lookup("ChangeTheme.TCombobox","foreground"),fieldbackground=root.style.colors.bg)
    change_text_size()  
   
def show_page(page,title):
    page.tkraise()
    page_title.config(text=title)

    if page == user_login_page or page == user_sign_in_page:
        sidebar.grid_remove()
        toggle_sidebar_frame.pack_forget()
        streak_frame.pack_forget()

    elif current_user is None:
        hide_streak()

    else:
        toggle_sidebar_frame.pack(side="left")
        streak_frame.pack(side="right")

def toggle_sidebar():
    if sidebar.winfo_ismapped():
        sidebar.grid_remove()

    else:
        sidebar.grid()

# - Sidebar content

settings_button = ttk.Button(sidebar,text="Settings",command=lambda: show_page(settings, "Settings"),style="Sidebar.TButton")
settings_button.grid(row=0,column=0,padx=10,pady=10,sticky="nsew")

home_button = ttk.Button(sidebar,text="Home",command=lambda: show_page(home, "routineR"),style="Sidebar.TButton")
home_button.grid(row=1,column=0,padx=10,pady=10,sticky="nsew")

calendar_button = ttk.Button(sidebar,text="Calendar",command=lambda: show_page(calendar, "Calendar"),style="Sidebar.TButton")
calendar_button.grid(row=2,column=0,padx=10,pady=10,sticky="nsew")

checklist_button = ttk.Button(sidebar,text="Checklist",command=lambda: show_page(checklist, "Checklist"),style="Sidebar.TButton")
checklist_button.grid(row=3,column=0,padx=10,pady=10,sticky="nsew")

current_tasks_button = ttk.Button(sidebar,text="Current tasks",command=lambda: show_page(current_tasks, "Current Tasks"),style="Sidebar.TButton")
current_tasks_button.grid(row=4,column=0,padx=10,pady=10,sticky="nsew")

help_button = ttk.Button(sidebar,text="Help",command=lambda: show_page(help, "Help"),style="Sidebar.TButton")
help_button.grid(row=5,column=0,padx=10,pady=10,sticky="nsew")

# - Header content

toggle_sidebar_button = ttk.Button(toggle_sidebar_frame,text="☰",command=toggle_sidebar,style="Sidebar.TButton")
toggle_sidebar_button.pack(side="left",padx=10,pady=10)

# - Title Header content

page_title = ttk.Label(title_frame,text="routineR",font=("Verdana",20,"bold"))
page_title.pack(side="left", padx=(0,10))

title_meter = ttk.Meter(title_frame,amountused=56,metersize=55,showtext=True,metertype="full",textfont=("Verdana",6,"bold"))
title_meter.pack(side="left",pady=10)

User_profile = ttk.Button(user_icon_frame,text="👤",command=lambda: show_page(user_page,"User"),style=("Usericon.TButton"))
User_profile.pack(side="left",pady=20)

streak_label = ttk.Label(streak_frame,text="🔥 10 days streak",font=("Verdana", 12, "bold"))
streak_label.pack(side="left",pady=20)


# - Settings content

settings_title = ttk.Label(settings,text="Appearance",font=("Verdana",18,"bold"))
settings_title.pack(pady=(20,30))

theme_drop_title = ttk.Label(settings,text="Theme editor",font=("Verdana",12,"bold"))
theme_drop_title.pack(pady=(20, 30))

theme_drop = ttk.Combobox(settings,values=list(theme_map.keys()),state="readonly",style="ChangeTheme.TCombobox")
theme_drop.pack()
theme_drop.bind("<<ComboboxSelected>>",change_theme)

text_size_label = ttk.Label(settings,text="Adjust sidebar text size",font=("Verdana",12,"bold"))
text_size_label.pack(pady=(20, 5))

mini_text_size = ttk.Label(settings,text="Only accepts values 1 to 20",font=("Verdana",9,"bold"))
mini_text_size.pack(pady=5)

text_size = ttk.Entry(settings,width=20)
text_size.pack(pady=(20, 30))

# - Keybinds

root.bind("<F11>", toggle_fullscreen)
text_size.bind("<KeyRelease>", change_text_size)

# - User content

user_text_frame = ttk.Frame(user_page)
user_text_frame.pack(pady=100)

user_button_frame = ttk.Frame(user_page)
user_button_frame.pack()

guest_frame = ttk.Frame(user_page)
guest_frame.pack()

user_title = ttk.Label(user_text_frame,text="You are currently not signed in",font=("Verdana",18,"bold"))
user_title.pack(pady=50)

user_title_description = ttk.Label(user_text_frame,text="Please sign in to use full access of the app",font=("Verdana",12,"bold"))
user_title_description.pack()

user_sign_up_button = ttk.Button(user_button_frame,text="Sign up",style=("User_button.TButton"),command=lambda: show_page(user_sign_in_page,"User sign in"),width=15)
user_sign_up_button.pack(side="left",padx=5)

user_login_button = ttk.Button(user_button_frame,text="Login",style=("User_button.TButton"),command=lambda: show_page(user_login_page,"User login"),width=15)
user_login_button.pack(side="left",padx=10)

guest_browse_button = ttk.Button(guest_frame,text="Browse features",style=("User_button.TButton"),width=15)
guest_browse_button.pack(side="bottom",pady=50)

# - User sign in content

username_sign_in_text = ttk.Frame(user_sign_in_page)
username_sign_in_text.pack(pady=30)

username_advice_text = ttk.Frame(user_sign_in_page)
username_advice_text.pack(pady=30)

password_sign_in_text = ttk.Frame(user_sign_in_page)
password_sign_in_text.pack(pady=60)

password_advice_text = ttk.Frame(user_sign_in_page)
password_advice_text.pack()

message_sign_in_frame = ttk.Frame(user_sign_in_page)
message_sign_in_frame.pack(pady=60,padx=50)

username_sign_in_title = ttk.Label(username_sign_in_text,text="Username",font=("Verdana",18,"bold"))
username_sign_in_title.pack()

username_sign_in_box = ttk.Entry(username_sign_in_text,width=50)
username_sign_in_box.pack()

username_sign_in_advice = ttk.Label(username_advice_text,text=" Usernames are not case-sensitive \n Usernames cannot have spaces or special characters \n Usernames must be between 5 and 20 characters long \n Usernames may only contain letters (A-Z), numbers (0-9), underscores (_), and periods (.)",font=("Verdana",12),justify="center")
username_sign_in_advice.pack()

password_sign_in_title = ttk.Label(password_sign_in_text,text="Password",font=("Verdana",18,"bold"))
password_sign_in_title.pack()

password_sign_in_box = ttk.Entry(password_sign_in_text,width=50)
password_sign_in_box.pack()

password_sign_in_advice = ttk.Label(password_advice_text,text=" Passwords are case-sensitive \n Passwords cannot have spaces \n Passwords must be between 8 and 30 characters long \n  Passwords must contain atleast 1 special character (e.g. !, @, #, $, %), 1 number (0-9) and 1 uppercase letter (A-Z)",font =("Verdana",12),justify="center")
password_sign_in_advice.pack()

user_sign_in_button = ttk.Button(user_sign_in_page,text="Sign up",style=("User_button.TButton"),width=15,command=sign_up_button)
user_sign_in_button.pack(pady=100)

message_sign_in_text = ttk.Label(message_sign_in_frame,text="",style=("Message_sign_in.TLabel"),font=("Verdana"))
message_sign_in_text.pack()

# - User login content

username_login_text = ttk.Frame(user_login_page)
username_login_text.pack(pady=60)

password_login_text = ttk.Frame(user_login_page)
password_login_text.pack(pady=70)

message_login_text_frame = ttk.Frame(user_login_page)
message_login_text_frame.pack(pady=70)

username_login_title = ttk.Label(username_login_text,text="Username",font=("Verdana",18,"bold"))
username_login_title.pack()

username_login_box = ttk.Entry(username_login_text,width=50)
username_login_box.pack()

password_login_title = ttk.Label(password_login_text,text="Password",font=("Verdana",18,"bold"))
password_login_title.pack()

password_login_box = ttk.Entry(password_login_text,width=50)
password_login_box.pack()

username_login_button = ttk.Button(user_login_page,text="Login",style=("User_button.TButton"),command=login_button,width=15)
username_login_button.pack()

message_login_text = ttk.Label(message_login_text_frame,text="",style=("Message_login.TLabel"),font=("Verdana"))
message_login_text.pack()

# - User post login content

logout_frame = ttk.Frame(user_page)
logout_frame.pack(pady=50)

logout_button = ttk.Button(logout_frame,text="Logout",style=("User_button.TButton"),command=logout,width=15)
logout_button.pack()

# - Checklist content

checklist_frame_box = ttk.Frame(checklist)
checklist_frame_box.pack(pady=(30,20))

checklist_box = ttk.Entry(checklist_frame_box,width=50)
checklist_box.pack(side="left",padx=5)

checklist_input_frame = ttk.Frame(checklist)
checklist_input_frame.pack(pady=10)

checklist_message_frame = ttk.Frame(checklist)
checklist_message_frame.pack(padx=20)

checklist_add_button = ttk.Button(checklist_input_frame,text="Add tasks",command=add_checklist_task,style="User_button.TButton")
checklist_add_button.pack(side="left",padx=5)

checklist_items_frame = ttk.Frame(checklist)
checklist_items_frame.pack(fill="both",expand=True,pady=30,padx=50)

checklist_message = ttk.Label(checklist_message_frame,text="",font=("Verdana",10,"bold"))
checklist_message.pack(pady=5)

# - Calender content

start_hour = 8
end_hour = 20

slot_height = 45
time_column_width = 70

week_dates = [current_week_start + timedelta(days=i) for i in range(7)]

calendar_navigation = ttk.Frame(calendar)
calendar_navigation.pack(fill="x",padx=30,pady=(20,0))

calendar_grid = ttk.Frame(calendar)
calendar_grid.pack(fill="both",expand=True,padx=30,pady=20)

calendar_grid.columnconfigure(0,minsize=time_column_width, weight=0)

for column in range(1,8):
    calendar_grid.columnconfigure(column,minsize=100,weight=1,uniform="days")

previous_calendar_button = ttk.Button(calendar_navigation,text="Previous",command= lambda: change_week(-1),style = "User_button.TButton")
previous_calendar_button.pack(side="left")

next_calendar_button = ttk.Button(calendar_navigation,text="Next", command= lambda: change_week(1), style = "User_button.TButton")
next_calendar_button.pack(side="right")

current_week_title = ttk.Label(calendar_navigation,text=current_week_start,font=("Verdana",14,"bold"))
current_week_title.pack(side="left",expand=True)

load_calendar()
hide_streak()
logout_frame.pack_forget()
sidebar.grid_remove()
home.tkraise()
root.protocol("WM_DELETE_WINDOW", close_app)
root.mainloop()
