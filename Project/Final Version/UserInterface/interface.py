import cv2  # Import the OpenCV library
import mediapipe as mp  # Import the Mediapipe library
import datetime  # Import the datetime module
import tkinter as tk  # Import the tkinter library
from PIL import Image, ImageTk  # Import the Image and ImageTk modules from the PIL library
from tkinter import ttk  # Import the ttk module from the tkinter library
from Model.HandPoseAnalyze import HandPoseAnalyzer  # Import the HandPoseAnalyzer class from the HandPoseAnalyze module
from Model.HandPoseDetector import h_gesture  # Import the h_gesture function from the HandPoseDetector module
from Model.HandPoseDetector import alignment_detection  # Import the alignment_detection function from the HandPoseDetector module

class HandGestureApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")  # Set the initial window size to 800x600 to fit the layout
        self.minsize(800, 600)  # Set the minimum window size to 800x600
        self.title("Hand Gesture Detector")  # Set the window title to "Hand Gesture Detector"
        self.init_ui()  # Initialize the user interface
        self.running = False  # Initialize the running state to False
        self.init_camera()  # Initialize the camera

    def init_ui(self):
        # Create a label frame for the video display area
        self.video_frame = ttk.LabelFrame(self, text="Video Display")
        self.video_frame.grid(row=0, column=0, padx=10, pady=10)
        self.canvas_width, self.canvas_height = 640, 480
        self.video_canvas = tk.Canvas(self.video_frame, width=self.canvas_width, height=self.canvas_height)
        self.video_canvas.pack()

        # Create a frame for the control buttons
        self.control_frame = ttk.Frame(self)
        self.control_frame.grid(row=0, column=1, sticky=tk.N)

        # Create start and stop buttons
        self.start_button = ttk.Button(self.control_frame, text="START", command=self.start_detection)
        self.stop_button = ttk.Button(self.control_frame, text="STOP", command=self.stop_detection)

        self.start_button.pack(fill=tk.X, pady=5)
        self.stop_button.pack(fill=tk.X, pady=5)

        # Create an output text area
        self.output_text = tk.Text(self, height=15, width=100)
        self.output_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.video_label = tk.Label(self.video_frame)
        self.video_label.pack()

    def init_camera(self):
        # Initialize the hand detector in the Mediapipe library
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75)

    def start_detection(self):
        if not self.running:
            self.running = True
            self.update_frame()

    def stop_detection(self):
        self.running = False
        self.output_text.delete('1.0', tk.END)

    def print_info(self, text):
        self.output_text.insert(tk.END, text + "\n")

    def update_frame(self):
        if self.running:
            ret, frame = True, cv2.VideoCapture(0).read()[1]
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.flip(frame, 1)
                results = self.hands.process(frame)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                        # Additional processing
                        hand_local = []
                        for i in range(21):
                            x = hand_landmarks.landmark[i].x * frame.shape[1]
                            y = hand_landmarks.landmark[i].y * frame.shape[0]
                            hand_local.append((x, y))

                        if hand_local:
                            angle_list, distance_48, distance_37, distance_26, distance_812, distance_1216, distance_1620 = HandPoseAnalyzer.hand_angle(hand_local)
                            gesture_str = h_gesture(angle_list, distance_48)
                            detection_result = alignment_detection(angle_list, distance_48)
                            info = f"Current Beijing Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                            info += f"Your Posture: {gesture_str}\n"
                            info += "Initial Hand Angles:\n"
                            info += f"Thumb Angle: {angle_list[0]}\n"
                            info += f"Index Finger Angle: {angle_list[1]}\n"
                            info += f"Middle Finger Angle: {angle_list[2]}\n"
                            info += f"Ring Finger Angle: {angle_list[3]}\n"
                            info += f"Pinky Finger Angle: {angle_list[4]}\n"
                            info += f"Thumb and Index Finger Distance: {distance_48}\n"
                            info += f"Suggestion For You: {detection_result}"
                            self.output_text.delete('1.0', tk.END)  # Clear previous content
                            self.output_text.insert(tk.END, info)  # Insert new content
            frame = cv2.resize(frame, (self.canvas_width, self.canvas_height))
            frame = Image.fromarray(frame)
            frame_image = ImageTk.PhotoImage(image=frame)
            if hasattr(self, 'canvas_image_id'):
                self.video_canvas.itemconfig(self.canvas_image_id, image=frame_image)
            else:
                self.canvas_image_id = self.video_canvas.create_image(0, 0, anchor='nw', image=frame_image)
            self.video_canvas.imgtk = frame_image  # Keep the reference
        self.after(33, self.update_frame)  # Continue looping

if __name__ == "__main__":
    app = HandGestureApp()
    app.mainloop()  # Run the main program loop

