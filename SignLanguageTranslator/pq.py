import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QHBoxLayout
import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

mp_holistic = mp.solutions.holistic  # Holistic model
mp_drawing = mp.solutions.drawing_utils  # Drawing utilities

def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False  # Image is no longer writeable
    results = model.process(image)  # Make prediction
    image.flags.writeable = True  # Image is now writeable
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # COLOR COVERSION RGB 2 BGR
    return image, results

def draw_styled_landmarks(image, results):
    # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                               mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                               mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2)
                               )
    # Draw right hand connections
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                               mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                               mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                               )

def extract_keypoints(results):
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21 * 3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21 * 3)
    return np.concatenate([lh, rh])

def process_words(words):
    special_cases = {
        ('happy', 'meet', 'you'): "Happy to meet you!",
        ('happy', 'meet','wrong', 'you'): "Happy to meet you!",
        ('how', 'you'): "How are you?",
        ('how', 'wrong', 'you'): "How are you?",
        ('how', 'null', 'you'): "How are you?",
        ('you', 'right'): "Are you right?",
        ('you', 'wrong'): "You are wrong!",
        ('like', 'you'): "I like you!",
        ('more', 'happy'): "Be more happy!"
    }

    # 遍历特殊情况字典中的每个键
    for key in special_cases.keys():
        # 遍历识别到的单词序列中的每个单词
        for i in range(len(words)):
            # 检查当前单词是否与特殊情况字典中的某个键的第一个单词匹配
            if words[i] == key[0]:
                # 检查剩余的单词是否依次匹配特殊情况字典中的键
                matched = True
                for j in range(1, len(key)):
                    if i+j >= len(words) or words[i+j] != key[j]:
                        matched = False
                        break
                # 如果匹配成功，则返回相应的话语
                if matched:
                    return special_cases[key]

    # 如果没有匹配的特殊情况，则返回None
    return None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hand Gesture Recognition")
        self.setStyleSheet("background-color: white;")  # 设置窗口背景颜色为白色

        # Create central widget and set layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # Create layout for video label and buttons
        video_button_layout = QVBoxLayout()
        layout.addLayout(video_button_layout)  # No alignment here

        self.video_label = QLabel()
        video_button_layout.addWidget(self.video_label)  # No alignment here

        # Set alignment for video_button_layout
        video_button_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)  # Align to top-left

        # Create button layout
        button_layout = QVBoxLayout()  # Changed to QVBoxLayout
        video_button_layout.addLayout(button_layout)  # Changed to addLayout

        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start_capture)
        button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop_capture)
        button_layout.addWidget(self.stop_button)
        self.stop_button.setEnabled(False)

        # Set button styles
        self.set_button_style(self.start_button)
        self.set_button_style(self.stop_button)

        # Create layout for output text boxes
        output_layout = QVBoxLayout()
        layout.addLayout(output_layout)

        self.gesture_output = QTextEdit()
        output_layout.addWidget(self.gesture_output)

        self.additional_output = QTextEdit()
        output_layout.addWidget(self.additional_output)

        # Set styles for output text boxes
        self.set_output_style(self.gesture_output)
        self.set_output_style(self.additional_output)

        # Initialize video capture and timer
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # Set mediapipe model
        self.holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        # Load gesture recognition model
        self.model = Sequential()
        self.model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(3, 126)))
        self.model.add(LSTM(128, return_sequences=True, activation='relu'))
        self.model.add(LSTM(64, return_sequences=False, activation='relu'))
        self.model.add(Dense(64, activation='relu'))
        self.model.add(Dense(32, activation='relu'))

        # Set actions array
        self.actions = np.array(['hello', 'happy', 'meet', 'you', 'like', 'how', 'more', 'two', 'three', 'no', 'right',
                                 'want', 'wrong', 'null'])
        self.model.add(Dense(self.actions.shape[0], activation='softmax'))
        self.model.load_weights('action.h5')

        # Initialize sequence and sentence for gesture recognition
        self.sequence = []
        self.sentence = []
        self.threshold = 0.95

        # Show empty black frame initially
        self.video_label.setPixmap(QPixmap(640, 480))

        # 记录输出的句子数量
        self.sentence_count = 0

    def set_button_style(self, button):
        button_font = QFont("Arial", 16, QFont.Bold)
        button.setFont(button_font)
        button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                border-radius: 15px;
                padding: 10px 20px;
                color: white;
            }

            QPushButton:hover {
                background-color: #0056b3;
            }

            QPushButton:pressed {
                background-color: #003d6e;
            }
        """)

    def set_output_style(self, output):
        output_font = QFont("Arial", 30)
        output.setFont(output_font)
        output.setStyleSheet("""
            QTextEdit {
                border: 2px solid #f0f0f0; /* Changed border color to match background */
                border-radius: 10px;
                background-color: #f0f0f0;
                padding: 5px;
            }
        """)

    def start_capture(self):
        self.timer.start(10)
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_capture(self):
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            image, results = mediapipe_detection(frame, self.holistic)
            draw_styled_landmarks(image, results)

            keypoints = extract_keypoints(results)
            self.sequence.append(keypoints)
            self.sequence = self.sequence[-3:]
            if len(self.sequence) == 3:
                res = self.model.predict(np.expand_dims(self.sequence, axis=0))[0]
                gesture = self.actions[np.argmax(res)]

                if res[np.argmax(res)] > self.threshold:
                    if len(self.sentence) > 0:
                        if gesture != self.sentence[-1]:
                            self.sentence.append(gesture)
                    else:
                        self.sentence.append(gesture)
                if len(self.sentence) > 5:
                    self.sentence = self.sentence[-5:]

                # 更新手势输出文本框
                self.gesture_output.clear()
                self.gesture_output.append(' '.join(self.sentence))

                # 处理句子并输出
                processed_sentence = process_words(self.sentence)
                if processed_sentence:
                    self.additional_output.append(processed_sentence)
                    self.sentence_count += 1
                    self.sentence = []

            h, w, c = image.shape
            bytes_per_line = c * w
            q_img = QImage(image.data, w, h, bytes_per_line, QImage.Format_BGR888)

            pixmap = QPixmap.fromImage(q_img)
            self.video_label.setPixmap(pixmap)
        else:
            self.video_label.setPixmap(QPixmap(640, 480))  # Show empty black frame if no frame available

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
