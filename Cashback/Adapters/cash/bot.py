import telebot 
from telebot import types
import os 
from google.oauth2 import service_account
from pydrive.drive import GoogleDrive
from io import BytesIO
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import re
import gspread
from datetime import datetime, date
import requests
import test
import threading

TOKEN = '6948251318:AAEX51QO6cPkuYUYMnNMkPFR_vGep3tOrrI'
EXISTING_FOLDER_ID = '1UzpUplg-dH1fnyiVOE-keFVT3k5nyT_q'
GOOGLE_DRIVE_CREDENTIALS_FILE = 'sshbot-401810-507d88f6b018.json'

credentials = service_account.Credentials.from_service_account_file(
    GOOGLE_DRIVE_CREDENTIALS_FILE,
    scopes=['https://www.googleapis.com/auth/drive']
)
drive_service = build('drive', 'v3', credentials=credentials)
bot = telebot.TeleBot(TOKEN)
drive:GoogleDrive

json_files={}


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
        bot.send_message(chat_id, "Great! Please upload the video for Kaspi (section: Акции).\nPlease note that the page need to be scrolled by one box.After scrolling through one complete box or section, stop")
        bot.register_next_step_handler_by_chat_id(chat_id, handle_video,call.data)
    elif call.data == 'Jusan':
        bot.send_message(chat_id, "Great! Please upload the video for Jusan (section: Акции).\nPlease note that the page need to be scrolled by one box.After scrolling through one complete box or section, stop")
        bot.register_next_step_handler_by_chat_id(chat_id, handle_video, call.data)

@bot.message_handler(content_types=['video'])
def handle_video(message, bank_name):
    # Access the video file
    
    file_id = message.video.file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    file_metadata = {
        'name': f"{bank_name}_received_video.mp4",
        'parents': [EXISTING_FOLDER_ID]  # Ensure you have the correct folder ID here
    }
    query = f"name='{file_metadata['name']}' and '{EXISTING_FOLDER_ID}' in parents and trashed=false"
    response = drive_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    for file in response.get('files', []):
        # Delete the file
        drive_service.files().delete(fileId=file['id']).execute()
    try:
        media_body = MediaIoBaseUpload(BytesIO(downloaded_file), mimetype='video/mp4', resumable=True)
        uploaded_file = drive_service.files().create(
            body=file_metadata,
            media_body=media_body
        ).execute()

        video_path=f'videos/{bank_name}_received_video.mp4'
        bot.reply_to(message, f"Video received and saved successfully to Google Drive.")

    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")

    # request = drive_service.files().get_media(fileId=uploaded_file['id'])
    # with open(video_path, 'wb') as f:
    #     downloader = MediaIoBaseDownload(f, request)
    #     done = False
    #     while done is False:
    #         status, done = downloader.next_chunk()
    # print("Download complete.")
    # json_files[bank_name]=test.get_data(bank_name,video_path)
    # print(json_files)
    # bot.send_message(message.chat.id, "Data extracted successfully. Type /send to upload another video.")

    # try:
    #     os.remove(video_path)
    #     print("File removed successfully")
    # except FileNotFoundError:
    #     print("File does not exist")
    # except PermissionError:
    #     print("Permission denied: cannot delete the file")
    # except Exception as e:
    #     print(f"Error occurred: {e}")
   





bot.polling(none_stop=True)




