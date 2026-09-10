from connection import supabase

def sign_up(username,password):
    try:
        username = username.lower() #Makes username case insensitive 

        if username == "" or password == "":  #Presence check
                return False, "Please enter your username and password", None
        
        if " " in username or " " in password:   #Space check
            return False, "Username and password must not contain spaces", None

        # Username validation

        if len(username) < 5 or len(username) > 20:
            return False, "Username must be between 5 and 20 characters", None

        if not all(char.isalnum() or char in "_." for char in username):
            return False, "Username must not have any spaces or special characters", None


        existing_user = (supabase.table("profiles").select("username").eq("username",username).execute()) #Checks if the username already exists 

        if existing_user.data:
            return False, "Username is already in use", None

        #Password validation

        if len(password) < 8 or len(password) > 30:
            return False, "Password must be betwen 8 and 30 characters", None

        if " " in password:
            return False, "Password must not contain spaces", None

        if not any(char.isupper() for char in password):
            return False, "Password must contain atleast 1 uppercase letter", None

        if not any(char.isdigit() for char in password):
            return False, "Password must contain atleast 1 number", None

        if not any(not char.isalnum() for char in password):
            return False, "Password must contain atleast 1 special character", None
    

        email = f"{username}@example.com" #Adds a pseudoemail 

        result = supabase.auth.sign_up({"email": email, "password": password, "options": {"data": {"username": username}}}) #Creates user auth account

        if result.user is None:
            return False, "Account could not be created", None

        return True, "Account successfully created", result.user

    except Exception as e:
        if "User already registered" in str(e):
            return False, "Username is already in use", None

        return False, "Account could not be created", None



def Login(username,password):
    username = username.lower()

    email = f"{username}@example.com"

    if username == "" or password == "":  #Presence check
        return False, "Please enter your username and password", None

    if " " in username or " " in password:   #Space check
        return False, "Username and password must not contain spaces", None

    try:
        result = supabase.auth.sign_in_with_password({"email": email, "password": password})

        if result.user is None: # If Supabase did not return a user
            return False, "Login failed", None

        return True, "Login successful", result.user

    except Exception:  #If the user did not fill out the right details
        return False, "Incorrect username or password", None

