#!/usr/bin/python3

import telebot
import subprocess
import datetime
import os

from keep_alive import keep_alive
keep_alive()

# Insert your Telegram bot token here
bot = telebot.TeleBot(os.getenv('7821207821:AAEr-kUcO3EyRaorgMP4-rFOJwOZA99KvRs'))

# Admin user IDs
admin_id = {"6386389835", "7417346403"}

# File to store allowed user IDs
USER_FILE = "users.txt"
FREE_USER_FILE = "free_users.txt"

# File to store command logs
LOG_FILE = "log.txt"

def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass

allowed_user_ids = read_users()

def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    username = "@" + user_info.username if user_info.username else f"UserID: {user_id}"
    with open(LOG_FILE, "a") as file:
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                return "Logs are already cleared. No data found. @PROxGOJOxAYUSH"
            else:
                file.truncate(0)
                return "Logs cleared successfully ✅ @PROxGOJOxAYUSH"
    except FileNotFoundError:
        return "No logs found to clear. @PROxGOJOxAYUSH"

def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"User {user_to_add} added successfully 👍. @PROxGOJOxAYUSH"
            else:
                response = "User already exists 🤦‍♂️. @PROxGOJOxAYUSH"
        else:
            response = "Please specify a user ID to add 😒. @PROxGOJOxAYUSH"
    else:
        response = "ONLY OWNER CAN USE. @PROxGOJOxAYUSH"
    bot.reply_to(message, response)

@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"User {user_to_remove} removed successfully 👍. @PROxGOJOxAYUSH"
            else:
                response = f"User {user_to_remove} not found in the list. @PROxGOJOxAYUSH"
        else:
            response = '''Please specify a user ID to remove.
✅ Usage: /remove <userid> @PROxGOJOxAYUSH'''
    else:
        response = "ONLY OWNER CAN USE. @PROxGOJOxAYUSH"
    bot.reply_to(message, response)

@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        response = clear_logs()
    else:
        response = "ONLY OWNER CAN USE. @PROxGOJOxAYUSH"
    bot.reply_to(message, response)

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                    response += "@PROxGOJOxAYUSH"
                else:
                    response = "No data found. @PROxGOJOxAYUSH"
        except FileNotFoundError:
            response = "No data found. @PROxGOJOxAYUSH"
    else:
        response = "ONLY OWNER CAN USE. @PROxGOJOxAYUSH"
    bot.reply_to(message, response)

@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found. @PROxGOJOxAYUSH"
                bot.reply_to(message, response)
        else:
            response = "No data found. @PROxGOJOxAYUSH"
            bot.reply_to(message, response)
    else:
        response = "ONLY OWNER CAN USE. @PROxGOJOxAYUSH"
        bot.reply_to(message, response)

@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"🤖Your ID: {user_id} @PROxGOJOxAYUSH"
    bot.reply_to(message, response)

def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"{username}, 𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.🔥🔥\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n𝐏𝐨𝐫𝐭: {port}\n𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: GOJO KA JADU @PROxGOJOxAYUSH"
    bot.reply_to(message, response)

bgmi_cooldown = {}
COOLDOWN_TIME = 300  # 5 minutes

@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        if user_id not in admin_id:
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < COOLDOWN_TIME:
                response = "You are on cooldown. Please wait 5 minutes before running the /bgmi command again. @PROxGOJOxAYUSH"
                bot.reply_to(message, response)
                return
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:
            target = command[1]
            port = int(command[2])
            time = int(command[3])
            if time > 3600:
                response = "Error: Time interval must be less than 3601. @PROxGOJOxAYUSH"
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)
        else:
            response = "Invalid command format. Use: /bgmi <target> <port> <time>@PROxGOJOxAYUSH"
    else:
        response = "You are not authorized to use this command. @PROxGOJOxAYUSH"
    bot.reply_to(message, response)

while True:
    try:
        bot.polling(none_stop=True)