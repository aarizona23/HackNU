import cv2
import PIL
import numpy as np
import google.generativeai as genai
from PIL import Image
from PIL import PngImagePlugin
import re
import json

api_url = 'AIzaSyB0ukVO8MdcOkcXuvFlEfatkQLw-0LxjZo'
genai.configure(api_key=api_url)

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


def get_response(bank_name):
    image= capture(f"videos/{bank_name}_received_video.mp4")

    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
    # response = model.generate_content(img)

    img = PIL.Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    response = model.generate_content(["Дай в формате: категория - % бонус - дата, убери из списка где проценты не уточняются", img], stream=True)
    response.resolve()

    return response.text

def get_cashbacks(bank):
    data = get_response(bank)
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
                "name": name,
                "bonus": bonus_match.group(1) if bonus_match else None,
                "date": date_match.group(1) if date_match else None
            }
            
            categories.append(category)
            print(category)
        
    return categories



def get_data_kaspi():
    data = get_cashbacks('Kaspi')
    json_string = json.dumps(data, indent=4, ensure_ascii=False)

    return json_string

def get_data_jusan():
    data = get_cashbacks('Jusan')
    json_string = json.dumps(data, indent=4, ensure_ascii=False)

    return json_string

print(get_data_kaspi())