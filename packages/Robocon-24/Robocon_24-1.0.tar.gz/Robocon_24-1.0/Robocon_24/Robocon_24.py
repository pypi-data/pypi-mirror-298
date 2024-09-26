import os
import requests
from pathlib import Path
from ultralytics import YOLO

# URL to download the model if not present
MODEL_URL = "https://drive.usercontent.google.com/uc?id=1igv9rp7LKlkLbGPbxvtM4D4DFM7wtQZy&export=download"
MODEL_NAME = "best.pt"

# Get the path to the user's cache directory
CACHE_DIR = Path.home() / ".cache" / "AI_models_Robocon_24"
MODEL_PATH = CACHE_DIR / MODEL_NAME

# Ensure the cache directory exists
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def download_model_if_not_exists():
    """Check if model exists, otherwise download it to cache folder."""
    if not MODEL_PATH.exists():
        print(f"Model not found at {MODEL_PATH}. Downloading...")
        response = requests.get(MODEL_URL, stream=True)
        if response.status_code == 200:
            # Write the model file to the cache directory
            with open(MODEL_PATH, 'wb') as model_file:
                for chunk in response.iter_content(chunk_size=8192):
                    model_file.write(chunk)
            print(f"Model downloaded successfully and saved to {MODEL_PATH}")
        else:
            raise RuntimeError(f"Failed to download the model. Status code: {response.status_code}")
    else:
        print(f"Model found at {MODEL_PATH}")

# Download the model if it doesn't exist
download_model_if_not_exists()

# Load the YOLO model from the cache
model = YOLO(str(MODEL_PATH))

def ball_detection(image):
    global model
    results = model.predict(image,conf = 0.3)
    results_image = results[0].plot()
    return results_image,results

def point_inside(rectangle, entire_coordinates):    
    x1, y1 ,x2, y2 , _ , _ = rectangle
    return (entire_coordinates[0] <= x1 <= entire_coordinates[2] and entire_coordinates[1] <= y1 <= entire_coordinates[3]) or (entire_coordinates[0] <= x2 <= entire_coordinates[2] and entire_coordinates[1] <= y2 <= entire_coordinates[3])

def get_rack_decision(balls_pattern,our_ball):
    
    ball_catagories = ['blue_ball','red_ball']
    
    my_ball_colour = ball_catagories[our_ball]
    opponent_ball_colour = ball_catagories[1 - our_ball]

    emtpy_racks = []
    my_ball_check_count = 0

    # finding empty racks
    for rack,ball_count in balls_pattern.items():
        if ball_count[my_ball_colour] != 0:
            my_ball_check_count += 1
        if ball_count[my_ball_colour] == 0 and ball_count[opponent_ball_colour] == 0:
            emtpy_racks.append(rack)

    # removing filled in racks
    for rack,ball_count in list(balls_pattern.items()):
        total_ball_count_in_rack = ball_count[my_ball_colour] + ball_count[opponent_ball_colour]
        if total_ball_count_in_rack == 3:
            balls_pattern.pop(rack)


    max_ball_list = []
    # rack finding logic
    if len(emtpy_racks) == 0 or my_ball_check_count >= 3:
        
        print("FIRST LOOP entered in after 3 ball placed in rack !!!!!!!!!!!!!!!!")
        
        for rack,ball_count in balls_pattern.items():
            count_my_ball = ball_count[my_ball_colour]
            count_opponent_ball = ball_count[opponent_ball_colour]
            
            if count_my_ball == 1 and count_opponent_ball == 1:
                sub_result = 2
            else:
                sub_result = count_my_ball - count_opponent_ball
 
            max_ball_list.append((rack,sub_result))
            
        
    if my_ball_check_count < 3 :
        
        print("SECOND LOOP entered in before first 3 ball placed in rack !!!!!!!!!!!!!!!!")
        
        for rack,ball_count in balls_pattern.items():
            count_my_ball = ball_count[my_ball_colour]
            count_opponent_ball = ball_count[opponent_ball_colour]
            
            if count_my_ball == 1 and count_opponent_ball == 1:
                sub_result = 2
                max_ball_list.append((rack,sub_result))
            
    if max_ball_list == []:
        keys_position = emtpy_racks[0]
    else:
        keys_position = max(max_ball_list, key=lambda x: x[1])[0]
        

    return keys_position

def decision_maker(image_input_def,our_ball):
    global model

    # initial balls pattern
    balls_pattern = {'rack_1': {'blue_ball':0,'red_ball':0}, 
                    'rack_2': {'blue_ball':0,'red_ball':0}, 
                    'rack_3': {'blue_ball':0,'red_ball':0}, 
                    'rack_4': {'blue_ball':0,'red_ball':0}, 
                    'rack_5': {'blue_ball':0,'red_ball':0}}
    
    input_image = image_input_def
    
    # model prediction
    results = model.predict(input_image,conf = 0.3,classes = [0,1,2])

    # find the position of the detected balls
    balls_detected_condinates = list(filter( lambda x: x[-1] != 2.0, results[0].boxes.numpy().data.tolist()))
    # find the position of the detected silos
    detected_silo_condinates = sorted(list(filter( lambda x: x[-1] == 2.0, results[0].boxes.numpy().data.tolist())),key=lambda x: x[0])

    # allow only five silo is detected
    if len(detected_silo_condinates) == 5: 
        
        finded_balls_in_silo = {}
        
        # adding the no of blue and red balls in each silo in the dictionary
        for id,i in enumerate(detected_silo_condinates):
            l = []
            d = {}
            for j in balls_detected_condinates:
                res_inside = point_inside(j,i)
                if res_inside:
                    l.append((j[-1]))
            blue_ball_count = l.count(0.0)
            red_ball_count = l.count(1.0)
            d['blue_ball'] = blue_ball_count
            d['red_ball'] = red_ball_count
            finded_balls_in_silo["rack_" + str(id + 1)] = d
            
        # adding finded_balls_in_silo in actual balls pattern
        balls_pattern['rack_1'] = finded_balls_in_silo['rack_1']
        balls_pattern['rack_2'] = finded_balls_in_silo['rack_2']
        balls_pattern['rack_3'] = finded_balls_in_silo['rack_3']
        balls_pattern['rack_4'] = finded_balls_in_silo['rack_4']
        balls_pattern['rack_5'] = finded_balls_in_silo['rack_5']
        
        keys_position = get_rack_decision(balls_pattern,our_ball)
  
    else:
        keys_position = 0        
        
    final_image_result  = results[0].plot()
    final_image_result = cv2.putText(final_image_result,str(keys_position),(450,400),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(255,0,0),thickness=1)
    return keys_position,final_image_result

