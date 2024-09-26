# is_sweep = "TT"
#
# sweep_yes_indicator = ["y", "yes", "true", "t", "1"]
# is_sweep = True if str(is_sweep).lower() in sweep_yes_indicator else False
# print(is_sweep)
import cv2
import os


# This function is to check frame rate of given video
def get_frame_rate(video_dir_input):
    try:
        cap_video = cv2.VideoCapture(video_dir_input)
    except Exception as e:
        print(e)
        return None
    if cap_video.isOpened():
        frame_rate = cap_video.get(cv2.CAP_PROP_FPS)
        return frame_rate
    else:
        return None


if __name__ == '__main__':
    dd = r"C:\Users\zawli\Desktop\ABI\Test_Folder\test_left_eye_v_2_0_DELL-S2716DG-11-06-2024_kids_long_screener_4th\pnm_eye_video.mp4"
    # dd = r"C:\Users\zawli\Desktop\ABI\Test_Folder\ahen_left_eye_v_1_4_1_kids_OS_right_sweep\pnm_eye_video.mp4"
    print("file exists?", os.path.exists(dd))
    ff = get_frame_rate(dd)
    print(ff)
