from ultralytics import YOLO
import cv2  # OpenCV library for webcam access
import numpy
cap = cv2.VideoCapture(2)

# Load a model
model = YOLO('yolov8n-pose.pt')  # load an official model

# Predict with the model
while True:
  # Read frame from webcam
  ret, frame = cap.read()

  # Check if frame is read successfully
  if not ret:
      print("Error: Unable to capture frame")
      break

  # Predict with YOLO model on the captured frame
  results = model(frame)
#   print(f"Class: {model.names[int(class_id)]}")
  # Process and display results (modify as needed)
#   for result in results:
#       Oframe = result.plot()
    #   result.show()  # Display detections on the frame
# Nose
# Left_Eye
# Right_Eye
# Left_Ear
# Right_Ear
# Left_Shoulder
# Right_Shoulder
# Left_Elbow
# Right_Elbow
# Left_Wrist
# Right_Wrist
# Left_Hip
# Right_Hip
# Left_Knee
# Right_Knee
# Left_Ankle
# Right_Ankle
  for result in results:
      Oframe = result.plot()
      points = result.keypoints.xy.numpy()
      Nose = points[0][0]
      Left_Eye = points[0][1]
      Right_Eye = points[0][2]
      Left_Ear = points[0][3]
      Right_Ear = points[0][4]
      Left_Shoulder = points[0][5]
      Right_Shoulder = points[0][6]
      Left_Elbow = points[0][7]
      Right_Elbow = points[0][8]
      Left_Wrist = points[0][9]
      Right_Wrist = points[0][10]
      Left_Hip = points[0][11]
      Right_Hip = points[0][12]
      Left_Knee = points[0][13]
      Right_Knee = points[0][14]
      Left_Ankle = points[0][15]
      Right_Ankle = points[0][16]
      print("all " , points,"nose ", points[0][0])

  # Display the webcam feed with detections (optional)
  cv2.imshow('Webcam Feed', Oframe)

  # Exit on 'q' key press
  if cv2.waitKey(1) == ord('q'):
      break

# Release resources
cap.release()
cv2.destroyAllWindows()


# results = model('https://ultralytics.com/images/bus.jpg')  # predict on an image
# for result in results:
#     result.show()