import cv2
import Robocon_24


# Open the camera
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Error: Could not open video stream from camera.")
    exit()

# Loop to continuously get frames
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Failed to capture image")
        break

    # Process the frame
    result, imgr = Robocon_24.decision_maker(image_input_def = frame, our_ball=0)
    
    # Display the result
    cv2.imshow('Processed Frame', imgr)

    # Print the result of decision_maker
    print(result)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
