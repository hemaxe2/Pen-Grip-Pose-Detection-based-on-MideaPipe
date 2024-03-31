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
    max_dis48 = 100

    #这些值都是我通过数据分析得到的一些大概的值，你们可以试着调整让他更加的精确，同时你们可以考虑引入其他的参数让你们的模型更加的完美

    gesture_str = "Wrong Posture"
    # If all angles and distances are within the correct range
    if 65535. not in angle_list:
        if (min_correct_tumb < angle_list[0] < max_correct_tumb) and \
                (min_correct_index < angle_list[1] < max_correct_index) and \
                (min_correct_middle < angle_list[2] < max_correct_middle) and \
                (min_correct_ring < angle_list[3] < max_correct_ring) and \
                (min_correct_pinky < angle_list[4] < max_correct_pinky) and \
                (distance_48 < max_dis48):
            gesture_str = "Correct Posture"

    return gesture_str

# Used to detect incorrect hand postures
def alignment_detection(angle_list, distance_48):
    min_correct_tumb = 30
    max_correct_tumb = 100
    min_correct_index = 80
    max_correct_index = 180
    min_correct_middle = 90
    max_correct_middle = 180
    min_correct_ring = 80
    max_correct_ring = 180
    min_correct_pinky = 80
    max_correct_pinky = 180
    max_dis48 = 100
    detection_result = ""

    if angle_list[0] < min_correct_tumb:
        detection_result += "Thumb angle too small. "
    elif angle_list[0] > max_correct_tumb:
        detection_result += "Thumb angle too large. "

    if angle_list[1] < min_correct_index:
        detection_result += "Index finger angle too small. "
    if angle_list[2] < min_correct_middle:
        detection_result += "Middle finger angle too small. "
    if angle_list[3] < min_correct_ring:
        detection_result += "Ring finger angle too small. "
    if angle_list[4] < min_correct_pinky:
        detection_result += "Pinky finger angle too small. "

    if distance_48 > max_dis48:
        detection_result += "Thumb and index finger distance too large. "

    return detection_result

    #这些建议知识一些例子，你们可以通过这些给出更加精确具体的例子，同时你们可以在此处加上语音播报的功能