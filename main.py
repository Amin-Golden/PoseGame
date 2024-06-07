import tkinter as tk
from tkinter import messagebox
import os
import ctypes
import cv2
from PIL import Image, ImageTk
from ultralytics import YOLO
import cv2  # OpenCV library for webcam access
import numpy
import time
from ahk import AHK
ahk = AHK()
global width ,height ,Pose_active , x1 , y1 , x2 , y2
Pose_active = 0  # Initialize Pose_active
x1 = 0
y1 = 0
x2  = 0
y2 = 0
def run_exe1():
    try:
        os.startfile(r"C:\Program Files (x86)\Fruit Ninja HD\FruitNinja.exe")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run the first exe: {e}")

def run_exe2():
    try:
        os.startfile(r"C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run the first exe: {e}")

def get_screen_size():
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    return screen_width, screen_height

def active_pose():
    global Pose_active
    Pose_active = 1
    messagebox.showinfo("Pose Estimation", f"Pose Estimation is Activated : {Pose_active}")
def deactive_pose():
    global Pose_active
    Pose_active = 0
    messagebox.showinfo("Pose Estimation", f"Pose Estimation is Deactivated : {Pose_active}")

def update_frame():
    global Pose_active , width ,height , x1 , y1 , x2 , y2
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)
        results = model(frame)

        for result in results:
            Oframe = result.plot()
            points = result.keypoints.xy.numpy()
            if len(points[0]) > 0 :
                # print("len ",len(points))
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
                # print("nose ", points[0][0])
                x,y = points[0][9]
                if ( Left_Wrist[0]!=0 and Left_Wrist[1]!=0 and Pose_active == 1 ):
                    # print("width",width,"height",height,"x",x,"y",y  ) 
                    last_x1 = x1
                    last_y1 = y1
                    x1 = width * Left_Wrist[0] / 640
                    y1 = height * Left_Wrist[1] / 480
                    # ahk.mouse_move(x, x, relative=False)
                    if(abs(last_x1 - x1) > 50 or abs(last_y1 - y1) > 50 ):
                        ahk.mouse_drag(x1, y1, relative=False)

                if ( Right_Wrist[0]!=0 and Right_Wrist[1]!=0 and Pose_active == 1 ):
                    # print("width",width,"height",height,"x",x,"y",y  ) 
                    last_x2 = x2
                    last_y2 = y2
                    x2 = width * Right_Wrist[0] / 640
                    y2 = height * Right_Wrist[1] / 480
                    # ahk.mouse_move(x, x, relative=False)
                    if(abs(last_x2 - x2) > 50 or abs(last_y2 - y2) > 50 ):
                        ahk.mouse_drag(x2, y2, relative=False)

        frame = cv2.cvtColor(Oframe, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        webcam_label.imgtk = imgtk
        webcam_label.configure(image=imgtk)
    webcam_label.after(10, update_frame)

# Initialize the main window
root = tk.Tk()
root.title("Pose Game ")

# Create and place the buttons
button1 = tk.Button(root, text="FruitNinja", command=run_exe1)
button1.pack(pady=10)

button2 = tk.Button(root, text="Run GAame 2", command=run_exe2)
button2.pack(pady=10)

button_mouse_active = tk.Button(root, text="Active Pose", command=active_pose)
button_mouse_active.pack(pady=10)

button_mouse_deactive = tk.Button(root, text="Deactive Pose", command=deactive_pose)
button_mouse_deactive.pack(pady=10)

# Create the webcam label
webcam_label = tk.Label(root)
webcam_label.pack(pady=10)

model = YOLO('yolov8n-pose.pt')  # load an official model
width, height = get_screen_size()
# Set up the webcam feed
cap = cv2.VideoCapture(2)
if not cap.isOpened():
    messagebox.showerror("Error", "Unable to access the webcam")
else:
    update_frame()

# Run the Tkinter event loop
root.mainloop()

# Release the webcam when the GUI is closed
cap.release()
cv2.destroyAllWindows()
