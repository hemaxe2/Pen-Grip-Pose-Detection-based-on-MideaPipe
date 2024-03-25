import cv2
import mediapipe as mp
import math
import pandas as pd

# 定义函数：计算两个二维向量之间的夹角
def vector_2d_angle(v1, v2):
    v1_x = v1[0]  # 第一个向量的x分量
    v1_y = v1[1]  # 第一个向量的y分量
    v2_x = v2[0]  # 第二个向量的x分量
    v2_y = v2[1]  # 第二个向量的y分量
    try:
        # 计算夹角并将弧度转换为角度
        angle_ = math.degrees(math.acos(
            (v1_x * v2_x + v1_y * v2_y) / (((v1_x ** 2 + v1_y ** 2) ** 0.5) * ((v2_x ** 2 + v2_y ** 2) ** 0.5))))
    except:
        angle_ = 65535.  # 如果出现异常，将角度设置为65535（表示无效角度）
    if angle_ > 180.:
        angle_ = 65535.  # 如果角度大于180度，将角度设置为65535（表示无效角度）
    return angle_

# 定义函数：计算两点之间的距离
def calculate_distance(point1, point2):
    dx = point2[0] - point1[0]  # 计算x方向上的距离
    dy = point2[1] - point1[1]  # 计算y方向上的距离
    distance = math.sqrt(dx ** 2 + dy ** 2)  # 计算距离
    return distance

# 定义函数：计算手部关节的角度
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

def h_gesture(angle_list, distance_48, distance_37, distance_26, distance_812, distance_1216, distance_1620):
    gesture_str = "Wrong Posture"
    return gesture_str

def detect():
    mp_drawing = mp.solutions.drawing_utils  # 导入绘图工具
    mp_hands = mp.solutions.hands  # 导入手部检测模型
    hands = mp_hands.Hands(
        static_image_mode=False,  # 静态图模式设为False，以处理连续视频帧
        max_num_hands=1,  # 最多检测的手的数量
        min_detection_confidence=0.75,  # 最小检测置信度阈值
        min_tracking_confidence=0.75)  # 最小跟踪置信度阈值

    cap = cv2.VideoCapture(0)  # 打开摄像头，参数为摄像头设备索引号，0代表第一个摄像头

    columns = ['Frame', 'Hand', 'Gesture', 'Thumb Angle', 'Index Angle', 'Middle Angle', 'Ring Angle', 'Pinky Angle',
               'Angle 5', 'Angle 6', 'Angle 7', 'Angle 8', 'Angle 9', 'Angle 10', 'Angle 11', 'Distance 48',
               'Distance 37', 'Distance 26', 'distance_812', 'distance_1216', 'distance_1620']

    data = []  # 存储手部数据的列表
    frame_count = 0  # 帧计数器

    while True:
        ret, frame = cap.read()  # 读取摄像头帧
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 将BGR格式转换为RGB格式
        frame = cv2.flip(frame, 1)  # 水平翻转图像（镜像）
        results = hands.process(frame)  # 处理当前帧的手部检测
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # 将RGB格式转换为BGR格式
        frame_count += 1  # 帧计数加1

        if results.multi_handedness:  # 如果检测到手部
            for hand_label, hand_landmarks in zip(results.multi_handedness, results.multi_hand_landmarks):
                hand_jugg = str(hand_label).split('"')[1]  # 提取手部侧重

                hand_local = []
                for i in range(21):  # 遍历21个手部关键点
                    x = hand_landmarks.landmark[i].x * frame.shape[1]  # 计算手部关键点在图像中的x坐标
                    y = hand_landmarks.landmark[i].y * frame.shape[0]  # 计算手部关键点在图像中的y坐标
                    hand_local.append((x, y))  # 将坐标添加到手部局部列表中

                if hand_local:  # 如果存在手部局部坐标
                    angle_list, distance_48, distance_37, distance_26, distance_812, distance_1216, distance_1620 = hand_angle(hand_local)  # 计算手部角度和距离
                    gesture_str = h_gesture(angle_list)  # 判断手势

                    # 将帧计数、手部侧重、手势类型、角度和距离数据添加到数据列表中
                    data.append([frame_count, hand_jugg, gesture_str] + angle_list + [distance_48, distance_37, distance_26, distance_812, distance_1216, distance_1620])

                    # 在图像上绘制手部关键点和连接线
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                                              mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2))

        cv2.imshow('MediaPipe Hands', frame)  # 显示带有手部标记的图像

        if cv2.waitKey(200) & 0xFF == 27:  # 按下ESC键时退出循环
            break

    cap.release()  # 释放摄像头
    cv2.destroyAllWindows()  # 关闭所有窗口

    # 将数据列表转换为DataFrame并保存为Excel文件
    df = pd.DataFrame(data, columns=columns)
    df.to_excel(' Correct hand_gestures_data.xlsx', index=False)


if __name__ == '__main__':
    detect()
