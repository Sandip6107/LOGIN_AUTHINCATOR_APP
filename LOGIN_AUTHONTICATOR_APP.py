import bcrypt
import re
from db import execute_query

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def validate_name(name):
    if not name:
        return False, "Name cannot be empty."
    if len(name) < 3:
        return False, "Name must be at least 3 characters long."
    if name.startswith(' '):
        return False, "Name cannot start with a space."
    if ' ' not in name:
        return False, "Name must contain at least one space (e.g., First Last)."
    if '  ' in name:
        return False, "Name cannot contain multiple consecutive spaces."
    return True, ""

def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search("[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search("[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search("[0-9]", password):
        return False, "Password must contain at least one number."
    return True, ""

def register_user(full_name, email, mobile, password, role='user'):
    is_name_valid, n_msg = validate_name(full_name)
    if not is_name_valid:
        return False, n_msg
        
    is_pwd_valid, p_msg = validate_password(password)
    if not is_pwd_valid:
        return False, p_msg
        
    pwd_hash = hash_password(password)
    
    query = "INSERT INTO users (full_name, email, mobile, password_hash, role) VALUES (%s, %s, %s, %s, %s)"
    params = (full_name, email, mobile, pwd_hash, role)
    
    result = execute_query(query, params)
    if result:
        return True, "Registration successful!"
    return False, "Registration failed. Email or mobile might already exist."

def login_user(email, password):
    query = "SELECT * FROM users WHERE email = %s"
    user = execute_query(query, (email,), fetch=True)
    
    if not user:
        return None, "User not found."
    
    user = user[0]
    
    if user['status'] == 'locked':
        # Check if 1 minute has passed since the last failed attempt
        last_attempt_query = "SELECT attempt_time FROM login_attempts WHERE user_id = %s AND status = 'failed' ORDER BY attempt_time DESC LIMIT 1"
        last_attempt_raw = execute_query(last_attempt_query, (user['id'],), fetch=True)
        
        if last_attempt_raw and last_attempt_raw[0]['attempt_time']:
            from datetime import datetime, timedelta
            last_attempt_time = last_attempt_raw[0]['attempt_time']
            if datetime.now() - last_attempt_time < timedelta(minutes=30):
                wait_time = timedelta(minutes=30) - (datetime.now() - last_attempt_time)
                minutes_left = int(wait_time.total_seconds() // 60)
                seconds_left = int(wait_time.total_seconds() % 60)
                return None, f"Account is locked due to many failed attempts. Try again in {minutes_left}m {seconds_left}s."
            else:
                # 30 minutes passed, unlock account
                execute_query("UPDATE users SET status = 'active', failed_attempts = 0 WHERE id = %s", (user['id'],))
                user['status'] = 'active'
                user['failed_attempts'] = 0
        else:
            return None, "Account is locked due to many failed attempts."
    
    if verify_password(password, user['password_hash']):
        # Reset failed attempts and update last login
        execute_query("UPDATE users SET failed_attempts = 0, last_login = CURRENT_TIMESTAMP WHERE id = %s", (user['id'],))
        # Log attempt
        execute_query("INSERT INTO login_attempts (user_id, status) VALUES (%s, 'success')", (user['id'],))
        return user, "Login successful!"
    else:
        # Increment failed attempts
        new_attempts = user['failed_attempts'] + 1
        status = 'locked' if new_attempts >= 3 else user['status']
        execute_query("UPDATE users SET failed_attempts = %s, status = %s WHERE id = %s", (new_attempts, status, user['id']))
        # Log attempt
        execute_query("INSERT INTO login_attempts (user_id, status) VALUES (%s, 'failed')", (user['id'],))
        
        msg = "Invalid password."
        if status == 'locked':
            msg = "Invalid password. Account is now locked for 30 minutes."
        return None, msg
