import telebot 
from telebot import types
import os 

TOKEN = '6948251318:AAEX51QO6cPkuYUYMnNMkPFR_vGep3tOrrI'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Type /send to start uploading the video.")

@bot.message_handler(commands=['send'])
def send_application(message):
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("Kaspi Bank", callback_data='Kaspi'),
               types.InlineKeyboardButton("Jusan", callback_data='Jusan'))
    bot.send_message(chat_id, "Select the Bank", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    if call.data == 'Kaspi':
        bot.send_message(chat_id, "Great! Please upload the video for Kaspi.\nPlease note that the page need to be scrolled by one box")
        bot.register_next_step_handler_by_chat_id(chat_id, handle_video,call.data)
    elif call.data == 'Jusan':
        bot.send_message(chat_id, "Great! Please upload the video for Jusan.\nPlease note that the page need to be scrolled by one box")
        bot.register_next_step_handler_by_chat_id(chat_id, handle_video, call.data)

@bot.message_handler(content_types=['video'])
def handle_video(message, bank_name):
    # Access the video file
    file_id = message.video.file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    directory = "videos"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save the video to a local file in the specified directory
    filepath = os.path.join(directory, f"{bank_name}_received_video.mp4")
    with open(filepath, "wb") as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, f"Video received and saved successfully in {filepath}!")

# Polling to keep the bot running
bot.polling(none_stop=True)