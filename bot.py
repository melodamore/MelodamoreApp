import os
import json
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Load allowed user IDs from the JSON file
def load_users():
    with open('auth_users.json', 'r') as file:
        data = json.load(file)
        return data['allowedUserIds']

# Save allowed user IDs to the JSON file
def save_users(user_ids):
    data = {'allowedUserIds': user_ids}
    with open('auth_users.json', 'w') as file:
        json.dump(data, file, indent=2)

# Command to add a user ID
def add_user(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    try:
        user_id = int(context.args[0])
        allowed_user_ids = load_users()

        if user_id not in allowed_user_ids:
            allowed_user_ids.append(user_id)
            save_users(allowed_user_ids)
            update.message.reply_text(f'User ID {user_id} has been added.')
        else:
            update.message.reply_text(f'User ID {user_id} is already in the list.')
    except (IndexError, ValueError):
        update.message.reply_text('Please provide a valid user ID.')

# Command to remove a user ID
def remove_user(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    try:
        user_id = int(context.args[0])
        allowed_user_ids = load_users()

        if user_id in allowed_user_ids:
            allowed_user_ids.remove(user_id)
            save_users(allowed_user_ids)
            update.message.reply_text(f'User ID {user_id} has been removed.')
        else:
            update.message.reply_text(f'User ID {user_id} is not in the list.')
    except (IndexError, ValueError):
        update.message.reply_text('Please provide a valid user ID.')

# Command to list all allowed user IDs
def list_users(update: Update, context: CallbackContext):
    allowed_user_ids = load_users()
    if allowed_user_ids:
        update.message.reply_text(f'Allowed User IDs:\n{", ".join(map(str, allowed_user_ids))}')
    else:
        update.message.reply_text('No users are currently allowed.')

# Command to help
def help_command(update: Update, context: CallbackContext):
    update.message.reply_text('Available commands:\n/add_user [userID]\n/remove_user [userID]\n/list_users\n/help')

# Main function to start the bot
def main():
    # Insert your Telegram bot token directly here
    token = '7771697129:AAEJukzZff1D-dBex9SrWkFUsu_AtPCnzH0'  # Replace with your actual token
    updater = Updater(token)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("add_user", add_user))
    dispatcher.add_handler(CommandHandler("remove_user", remove_user))
    dispatcher.add_handler(CommandHandler("list_users", list_users))
    dispatcher.add_handler(CommandHandler("help", help_command))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
