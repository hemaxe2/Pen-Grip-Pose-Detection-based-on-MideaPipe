import cv2
import mediapipe as mp
import math

def vector_2d_angle(v1, v2):
    '''
    求解二维向量的角度
    '''
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        angle_ = math.degrees(math.acos((v1_x * v2_x + v1_y * v2_y) / (((v1_x**2 + v1_y**2)**0.5) * ((v2_x**2 + v2_y**2)**0.5))))
    except:
        angle_ = 65535.
    if angle_ > 180.:
        angle_ = 65535.
    return angle_

def calculate_distance(point1, point2):
    '''
    计算两点之间的欧氏距离
    '''
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    distance = math.sqrt(dx**2 + dy**2)
    return distance

def hand_angle(hand_):
    angle_list = []  # 存储角度的列表

    # 计算手指之间的角度
    angle_0 = vector_2d_angle(((hand_[0][0] - hand_[2][0]), (hand_[0][1] - hand_[2][1])),
                              ((hand_[3][0] - hand_[4][0]), (hand_[3][1] - hand_[4][1])))
    angle_list.append(angle_0)

    angle_1 = vector_2d_angle(((hand_[0][0] - hand_[6][0]), (hand_[0][1] - hand_[6][1])),
                              ((hand_[7][0] - hand_[8][0]), (hand_[7][1] - hand_[8][1])))
    angle_list.append(angle_1)

    angle_2 = vector_2d_angle(((hand_[0][0] - hand_[10][0]), (hand_[0][1] - hand_[10][1])),
                              ((hand_[11][0] - hand_[12][0]), (hand_[11][1] - hand_[12][1])))
    angle_list.append(angle_2)

    angle_3 = vector_2d_angle(((hand_[0][0] - hand_[14][0]), (hand_[0][1] - hand_[14][1])),
                              ((hand_[15][0] - hand_[16][0]), (hand_[15][1] - hand_[16][1])))
    angle_list.append(angle_3)

    angle_4 = vector_2d_angle(((hand_[0][0] - hand_[18][0]), (hand_[0][1] - hand_[18][1])),
                              ((hand_[19][0] - hand_[20][0]), (hand_[19][1] - hand_[20][1])))
    angle_list.append(angle_4)

    # 计算手指关节之间的角度
    angle_5 = vector_2d_angle(((hand_[0][0] - hand_[2][0]), (hand_[0][1] - hand_[2][1])),
                              ((hand_[2][0] - hand_[3][0]), (hand_[2][1] - hand_[3][1])))
    angle_list.append(angle_5)

    angle_6 = vector_2d_angle(((hand_[2][0] - hand_[3][0]), (hand_[2][1] - hand_[3][1])),
                              ((hand_[3][0] - hand_[4][0]), (hand_[3][1] - hand_[4][1])))
    angle_list.append(angle_6)

    angle_7 = vector_2d_angle(((hand_[0][0] - hand_[5][0]), (hand_[0][1] - hand_[5][1])),
                              ((hand_[7][0] - hand_[8][0]), (hand_[7][1] - hand_[8][1])))
    angle_list.append(angle_7)

    angle_8 = vector_2d_angle(((hand_[5][0] - hand_[6][0]), (hand_[5][1] - hand_[6][1])),
                              ((hand_[7][0] - hand_[8][0]), (hand_[7][1] - hand_[8][1])))
    angle_list.append(angle_8)

    angle_9 = vector_2d_angle(((hand_[5][0] - hand_[6][0]), (hand_[5][1] - hand_[6][1])),
                              ((hand_[6][0] - hand_[7][0]), (hand_[6][1] - hand_[7][1])))
    angle_list.append(angle_9)

    angle_10 = vector_2d_angle(((hand_[6][0] - hand_[7][0]), (hand_[6][1] - hand_[7][1])),
                               ((hand_[7][0] - hand_[8][0]), (hand_[7][1] - hand_[8][1])))
    angle_list.append(angle_10)

    angle_11 = vector_2d_angle(((hand_[0][0] - hand_[9][0]), (hand_[0][1] - hand_[9][1])),
                               ((hand_[11][0] - hand_[12][0]), (hand_[11][1] - hand_[12][1])))
    angle_list.append(angle_11)

    # 计算手指关节之间的距离
    distance_48 = calculate_distance(hand_[4], hand_[8])
    distance_37 = calculate_distance(hand_[3], hand_[7])
    distance_26 = calculate_distance(hand_[2], hand_[6])
    distance_812 = calculate_distance(hand_[8], hand_[12])
    distance_1216 = calculate_distance(hand_[12], hand_[16])
    distance_1620 = calculate_distance(hand_[16], hand_[20])

    return angle_list, distance_48, distance_37, distance_26, distance_812, distance_1216, distance_1620

def h_gesture(angle_list, distance_48):
    min_correct_tumb = 30
    max_correct_tumb = 100
    min_correct_index = 80
    max_correct_index = 180
    min_correct_middle = 90
    max_correct_middle = 180
    min_correct_ring = 80
    max_correct_ring =180
    min_correct_pinky = 80
    max_correct_pinky = 180
    min_correct_angle7 = 80
    max_correct_angle7 = 100
    min_correct_angle11 = 100
    max_correct_angle11 = 180
    max_dis48 = 100

    gesture_str = "Wrong Posture"
    if 65535. not in angle_list:

        if (min_correct_tumb < angle_list[0] < max_correct_tumb) and (min_correct_index < angle_list[1] <
                max_correct_index) and (min_correct_middle < angle_list[2] < max_correct_middle) and (min_correct_ring <
                angle_list[3] < max_correct_ring) and (min_correct_pinky < angle_list[4] < max_correct_pinky)  (distance_48 < max_dis48):
            gesture_str = "Correct Posture"

            # and (min_correct_angle7 < angle_list[7] < max_correct_angle7 ) and (min_correct_angle11 < angle_list[11]
            #< max_correct_angle11) and 



    return gesture_str

def detect():
    # 初始化MediaPipe Hands模型
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75)

    # 打开摄像头
    cap = cv2.VideoCapture(0)

    while True:
        # 读取摄像头帧
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        results = hands.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # 获取手势标签
        if results.multi_handedness:
            for hand_label in results.multi_handedness:
                hand_jugg = str(hand_label).split('"')[1]
                print(hand_jugg)
                cv2.putText(frame, hand_jugg, (50, 200), 0, 1.3, (0, 0, 255), 2)

        # 获取手部关键点
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # 修改绘制手部关键点的颜色
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                           mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                                           mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2))

                hand_local = []
                for i in range(21):
                    x = hand_landmarks.landmark[i].x * frame.shape[1]
                    y = hand_landmarks.landmark[i].y * frame.shape[0]
                    hand_local.append((x, y))

                if hand_local:
                    angle_list, distance_48, distance_37, distance_26, distance_812, distance_1216, distance_1620 = hand_angle(
                        hand_local)
                    gesture_str = h_gesture(angle_list, distance_48)
                    print(gesture_str)
                    cv2.putText(frame, gesture_str, (50, 100), 0, 1.3, (0, 0, 255), 2)

        cv2.imshow('MediaPipe Hands', frame)

        if cv2.waitKey(200) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    detect()

