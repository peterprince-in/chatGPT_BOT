from dotenv import load_dotenv
import os
from typing import Final
import logging
from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes
from aiogram import Bot, Dispatcher, types
from telegram import InputFile

load_dotenv()
API_TOKEN = os.getenv("TOKEN")
bot = Bot(token=API_TOKEN)

#logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
BOT_USERNAME: Final = '@Notifierboss_bot'
#dp = Dispatcher(bot)

#commmands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("hello I am a bot thanks for talking with me")


#responses
def handle_response(text: str) ->str:
    processed: str = text.lower()
    if 'hello' in processed:
        return 'Hello, how are you'
    if 'bye' in processed:
        return 'see you later'
    
    return 'I do not understand'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.message.chat
    message_type = chat.type
    text = update.message.text

    user_id = chat.id
    username = chat.username
    full_name = chat.full_name if chat.full_name else "N/A"
    bio = chat.bio if chat.bio else "N/A"

    print(f'User({user_id}) in {message_type} - Text: "{text}"')
    print(f'Username: {username}, Full Name: {full_name}, Bio: {bio}')

    if message_type == 'group' and BOT_USERNAME in text:
        new_text = text.replace(BOT_USERNAME, '').strip()
        response = handle_response(new_text)
    elif message_type != 'group':
        response = handle_response(text)
    else:
        return

    print('Bot:', response)
    await update.message.reply_text(response)



async def get_user_profile_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    if user:
        photos = await context.bot.get_user_profile_photos(user.id)
        if photos and photos.photos:
            photo = photos.photos[0][-1]  # Get the highest resolution of the first profile photo
            file = await context.bot.get_file(photo.file_id)
            file_path = 'user_profile_picture.jpg'
            await file.download(file_path)  # Save the profile picture to a file
            with open(file_path, 'rb') as photo_file:
                await update.message.reply_photo(photo=InputFile(photo_file))
        else:
            await update.message.reply_text('You do not have a profile picture.')
    else:
        print('User information is not available.')

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update{update} caused error {context.error}')

#commands
if __name__=='__main__':
    print('starting bot...')
    app = Application.builder().token(API_TOKEN).build()

    #commands
    app.add_handler(CommandHandler('start',start_command))

    #message
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #errors
    app.add_error_handler(error)

    app.add_handler(CommandHandler('get_profile_picture', get_user_profile_photo))


    #Updates
    print('Polling...')
    app.run_polling(poll_interval=3)
