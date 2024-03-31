import math


class HandPoseAnalyzer:
    def __init__(self):
        pass

    @staticmethod
    # Calculate the angle between two 2D vectors
    def vector_2d_angle(v1, v2):
        v1_x = v1[0]
        v1_y = v1[1]
        v2_x = v2[0]
        v2_y = v2[1]
        try:
            angle_ = math.degrees(math.acos(
                (v1_x * v2_x + v1_y * v2_y) / (((v1_x ** 2 + v1_y ** 2) ** 0.5) * ((v2_x ** 2 + v2_y ** 2) ** 0.5))))
        except:
            angle_ = 65535.
        if angle_ > 180.:
            angle_ = 65535.

        return angle_

    @staticmethod
    # Calculate the distance between two points
    def calculate_distance(point1, point2):
        dx = point2[0] - point1[0]
        dy = point2[1] - point1[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)

        return distance

    @staticmethod
    # Calculate angle and distance of hand pose
    def hand_angle(hand_):
        angle_list = []

        angle_0 = HandPoseAnalyzer.vector_2d_angle(((hand_[0][0] - hand_[2][0]), (hand_[0][1] - hand_[2][1])),
                                                   ((hand_[3][0] - hand_[4][0]), (hand_[3][1] - hand_[4][1])))
        angle_list.append(angle_0)

        angle_1 = HandPoseAnalyzer.vector_2d_angle(((hand_[0][0] - hand_[6][0]), (hand_[0][1] - hand_[6][1])),
                                                   ((hand_[7][0] - hand_[8][0]), (hand_[7][1] - hand_[8][1])))
        angle_list.append(angle_1)

        angle_2 = HandPoseAnalyzer.vector_2d_angle(((hand_[0][0] - hand_[10][0]), (hand_[0][1] - hand_[10][1])),
                                                   ((hand_[11][0] - hand_[12][0]), (hand_[11][1] - hand_[12][1])))
        angle_list.append(angle_2)

        angle_3 = HandPoseAnalyzer.vector_2d_angle(((hand_[0][0] - hand_[14][0]), (hand_[0][1] - hand_[14][1])),
                                                   ((hand_[15][0] - hand_[16][0]), (hand_[15][1] - hand_[16][1])))
        angle_list.append(angle_3)

        angle_4 = HandPoseAnalyzer.vector_2d_angle(((hand_[0][0] - hand_[18][0]), (hand_[0][1] - hand_[18][1])),
                                                   ((hand_[19][0] - hand_[20][0]), (hand_[19][1] - hand_[20][1])))
        angle_list.append(angle_4)

        angle_5 = HandPoseAnalyzer.vector_2d_angle(((hand_[0][0] - hand_[2][0]), (hand_[0][1] - hand_[2][1])),
                                                   ((hand_[2][0] - hand_[3][0]), (hand_[2][1] - hand_[3][1])))
        angle_list.append(angle_5)

        angle_6 = HandPoseAnalyzer.vector_2d_angle(((hand_[2][0] - hand_[3][0]), (hand_[2][1] - hand_[3][1])),
                                                   ((hand_[3][0] - hand_[4][0]), (hand_[3][1] - hand_[4][1])))
        angle_list.append(angle_6)

        angle_7 = HandPoseAnalyzer.vector_2d_angle(((hand_[0][0] - hand_[5][0]), (hand_[0][1] - hand_[5][1])),
                                                   ((hand_[7][0] - hand_[8][0]), (hand_[7][1] - hand_[8][1])))
        angle_list.append(angle_7)

        angle_8 = HandPoseAnalyzer.vector_2d_angle(((hand_[5][0] - hand_[6][0]), (hand_[5][1] - hand_[6][1])),
                                                   ((hand_[7][0] - hand_[8][0]), (hand_[7][1] - hand_[8][1])))
        angle_list.append(angle_8)

        angle_9 = HandPoseAnalyzer.vector_2d_angle(((hand_[5][0] - hand_[6][0]), (hand_[5][1] - hand_[6][1])),
                                                   ((hand_[6][0] - hand_[7][0]), (hand_[6][1] - hand_[7][1])))
        angle_list.append(angle_9)

        angle_10 = HandPoseAnalyzer.vector_2d_angle(((hand_[6][0] - hand_[7][0]), (hand_[6][1] - hand_[7][1])),
                                                    ((hand_[7][0] - hand_[8][0]), (hand_[7][1] - hand_[8][1])))
        angle_list.append(angle_10)

        angle_11 = HandPoseAnalyzer.vector_2d_angle(((hand_[0][0] - hand_[9][0]), (hand_[0][1] - hand_[9][1])),
                                                    ((hand_[11][0] - hand_[12][0]), (hand_[11][1] - hand_[12][1])))
        angle_list.append(angle_11)

        distance_48 = HandPoseAnalyzer.calculate_distance(hand_[4], hand_[8])
        distance_37 = HandPoseAnalyzer.calculate_distance(hand_[3], hand_[7])
        distance_26 = HandPoseAnalyzer.calculate_distance(hand_[2], hand_[6])
        distance_812 = HandPoseAnalyzer.calculate_distance(hand_[8], hand_[12])
        distance_1216 = HandPoseAnalyzer.calculate_distance(hand_[12], hand_[16])
        distance_1620 = HandPoseAnalyzer.calculate_distance(hand_[16], hand_[20])

        return angle_list, distance_48, distance_37, distance_26, distance_812, distance_1216, distance_1620

    #所有的点位请参考mediapipe的21个点位图，在这里只有我认为应该要考虑到的在手势中的那些角度和距离，你可以参考我的代码加入更多的角度和距离
    #或者你可以通过其它的方法来判断