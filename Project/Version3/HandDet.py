import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import mediapipe as mp
from HandRec2 import hand_angle, h_gesture, alignment_detection  # Your functions from HandRec2.py

class HandGestureApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")  # Set a starting size for the window that fits the layout
        self.minsize(800, 600)
        self.title("Hand Gesture Detector")
        self.init_ui()
        self.running = False
        self.init_camera()

    def init_ui(self):
        self.video_frame = ttk.LabelFrame(self, text="Video Feed")
        self.video_frame.grid(row=0, column=0, padx=10, pady=10)
        self.canvas_width, self.canvas_height = 640, 480
        self.video_canvas = tk.Canvas(self.video_frame, width=self.canvas_width, height=self.canvas_height)
        self.video_canvas.pack()

        self.control_frame = ttk.Frame(self)
        self.control_frame.grid(row=0, column=1, sticky=tk.N)

        self.start_button = ttk.Button(self.control_frame, text="Start", command=self.start_detection)
        self.stop_button = ttk.Button(self.control_frame, text="Stop", command=self.stop_detection)
        self.pause_button = ttk.Button(self.control_frame, text="Pause", command=self.pause_detection)
        self.output_button = ttk.Button(self.control_frame, text="Output", command=self.output_results)

        
        self.start_button.pack(fill=tk.X, pady=5)
        self.stop_button.pack(fill=tk.X, pady=5)
        self.pause_button.pack(fill=tk.X, pady=5)
        self.output_button.pack(fill=tk.X, pady=5)

        self.output_text = tk.Text(self, height=10, width=50)
        self.output_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        
        self.video_label = tk.Label(self.video_frame)
        self.video_label.pack()

    def init_camera(self):
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
            self.cap = cv2.VideoCapture(0)
            self.update_frame()

    def stop_detection(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.video_label.configure(image=None)
        self.output_text.delete('1.0', tk.END)

    def pause_detection(self):
        # Pause the camera detection loop
        self.running = not self.running
        # ... your pause logic here

    def output_results(self):
        pass
        # Output the hand gesture status to the output_text widget
        # ... your output logic here (maybe call print_initial_info)


     
    def update_frame(self):
        if self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.flip(frame, 1)
                results = self.hands.process(frame)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                        # Additional processing
                        # ...

                frame = cv2.resize(frame, (self.canvas_width, self.canvas_height))
                frame = Image.fromarray(frame)
                frame_image = ImageTk.PhotoImage(image=frame)
                if hasattr(self, 'canvas_image_id'):
                    self.video_canvas.itemconfig(self.canvas_image_id, image=frame_image)
                else:
                    self.canvas_image_id = self.video_canvas.create_image(0, 0, anchor='nw', image=frame_image)
                self.video_canvas.imgtk = frame_image  # Keep reference

            self.after(33, self.update_frame)  # Continue the loop

    def update_gesture_status(self, gesture_info):
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, gesture_info)
        
        
    

if __name__ == '__main__':
    app = HandGestureApp()
    app.geometry("800x800")  # Set this to your desired initial size
    app.resizable(False, False)  # Prevent resizing
    app.mainloop()