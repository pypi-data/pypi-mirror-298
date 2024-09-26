from ultralytics import YOLO

model = YOLO(r"models\best_2.pt")

def ball_detection(image):
    global model
    results = model.predict(image,conf = 0.3)
    results_image = results[0].plot()
    return results_image,results


