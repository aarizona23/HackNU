import cv2
import PIL
import numpy as np
import google.generativeai as genai
from PIL import Image
from PIL import PngImagePlugin
import re
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account
import io
from googleapiclient.http import MediaIoBaseDownload
import os



folder_id='1UzpUplg-dH1fnyiVOE-keFVT3k5nyT_q'
json_files={}

api_url = 'AIzaSyB0ukVO8MdcOkcXuvFlEfatkQLw-0LxjZo'
genai.configure(api_key=api_url)

def setup_google_drive_client():
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = '/Users/arianasadyr/HackNU/Cashback/Adapters/cash/sshbot-401810-507d88f6b018.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    drive_service = build('drive', 'v3', credentials=credentials)
    return drive_service

# Function to list files in a specific Google Drive folder
def list_files_in_folder(drive_service, folder_id):
    query = f"'{folder_id}' in parents and trashed=false and mimeType='video/mp4'"
    results = drive_service.files().list(q=query, spaces='drive', fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    return items


def download_file(drive_service, file_id, file_name):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    with open(file_name, 'wb') as f:
        f.write(fh.read())
    print(f"Downloaded {file_name}")



def initialize_sift():
    return cv2.SIFT_create()

def sift_feature_matching(sift, img1, img2):
    # Detect features and compute descriptors.
    keypoints1, descriptors1 = sift.detectAndCompute(img1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(img2, None)
    
    # Create BFMatcher and match descriptors.
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)

    # Apply Lowe's ratio test.
    good_matches = 0
    for m, n in matches:
        if m.distance < 0.4 * n.distance:
            good_matches = good_matches + 1

    return good_matches

def capture(video_path):
    cap = cv2.VideoCapture(video_path)

    ret, prev_frame = cap.read()
    prev_frame = prev_frame[int(prev_frame.shape[0]*0.08):int(prev_frame.shape[0]*0.92), :]
    frames = [prev_frame]

    while True:
        prev_frame = cv2.cvtColor(frames[-1], cv2.COLOR_BGR2GRAY)
        ret, frame = cap.read()
        if not ret:
            break
        frame = frame[int(frame.shape[0]*0.08):int(frame.shape[0]*0.92), :]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        #compare structural similarity between two images
        sum_diff = cv2.matchTemplate(prev_frame, gray, cv2.TM_CCOEFF_NORMED)
        
        # Check if the frame has minimal differences
        if sum_diff[0][0] < -0.1:
            frames.append(frame)

    cap.release()


    prev_frame = frames[0]

    unique_frames = [prev_frame]
    sift = initialize_sift()  # Initialize SIFT detector

    for i in range(1, len(frames)):
        curr_frame = frames[i]
        img2 = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        img1 = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        num_matches = sift_feature_matching(sift, img1, img2)
        if num_matches < 500:
            unique_frames.append(curr_frame)
            
        prev_frame = curr_frame


    total_concatenated = np.concatenate(unique_frames, axis=1)
    return total_concatenated


def get_response(video_path):
    image= capture(video_path)

    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
    # response = model.generate_content(img)

    img = PIL.Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    response = model.generate_content(["Дай в формате: категория - % бонус - дата, убери из списка где проценты не уточняются", img], stream=True)
    response.resolve()

    return response.text

def get_cashbacks(bank, video_path):
    data = get_response(video_path)
    print(data)
    
    categories = []
    
    for line in data.strip().split('\n'):
        name_match = re.search(r'\*\s+\*\*(.*?)\*\*[:-]?\s*(.*)', line)
        if not name_match:
            continue
        
        name = name_match.group(1).strip()

        extra_info = name_match.group(2).strip()

        bonus_match = re.search(r'(\d+%)', extra_info)

        date_match = re.search(r'(\d+\s+\w+\s*-\s*\d+\s+\w+)', extra_info)

        
        # Create the category dictionary
        if bonus_match:
            category = {
                "category": name,
                "percentage": bonus_match.group(1) if bonus_match else None,
                "bank_name": bank,
                "valid_from": date_match.group(1) if date_match else None,
                "company" : None,
                "min_purchase_amount": None,
                "valid_to": None, 
                "payment_method": None,
                "days_of_week": None,
                "bank_type": None
            }
            
            categories.append(category)
            print(category)
        
    return categories



def get_data(bank_name,video_path):
    data = get_cashbacks(bank_name,video_path)
    json_string = json.dumps(data, indent=4, ensure_ascii=False)

    return json_string


def process_videos_from_drive(folder_id='1UzpUplg-dH1fnyiVOE-keFVT3k5nyT_q',bank_name='Kaspi'):
    drive_service = setup_google_drive_client()
    video_files = list_files_in_folder(drive_service, folder_id)

    for video in video_files:
        file_name = f"/Users/arianasadyr/HackNU/Cashback/Adapters/cash/videos/{video['name']}"
        download_file(drive_service, video['id'], file_name)
        data = get_data(video['name'].split('_')[0], file_name)  # Assuming get_data processes the video and returns JSON
        json_files[video['name'].split('_')[0]] = data
        
        try:
            os.remove(file_name)
            print("File removed successfully")
        except FileNotFoundError:
            print("File does not exist")
        except PermissionError:
            print("Permission denied: cannot delete the file")
        except Exception as e:
            print(f"Error occurred: {e}")
        
        if video['name'].split('_')[0] == bank_name:
            return data



def get_json(bank_name):
    
    return process_videos_from_drive(bank_name=bank_name)

get_json('Kaspi')

