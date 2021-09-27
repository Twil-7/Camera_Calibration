import numpy as np
import cv2
import time


if __name__ == "__main__":

    # 调用海康摄像头配置
    cap = cv2.VideoCapture("rtsp://admin:123456abc@192.168.1.120/h264/ch1/main/av_stream")

    frame_height = cap.get(3)    # 3代表帧的宽度， 2560.0
    frame_width = cap.get(4)     # 4代表帧的高度， 1440.0
    frame_fps = cap.get(5)       # 5代表帧速FPS， 8.0
    print(frame_fps, frame_width, frame_height)    # 8.0 1440.0 2560.0

    # mtx  : 相机内参矩阵
    # dist : 相机畸变系数
    mtx = np.array([[8.45559259e+02, 0.00000000e+00, 1.32460030e+03],
                    [0.00000000e+00, 8.50592806e+02, 7.29938055e+02],
                    [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
    dist = np.array([[-1.12961572e-01, 1.54572487e-02, -1.66183578e-03, -1.09252844e-04, -1.15994476e-03]])

    while True:

        ret, frame = cap.read()    # (1440, 2560, 3)

        h, w = frame.shape[:2]

        new_camera_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 0.2, (w, h))
        dst = cv2.undistort(frame, mtx, dist, None, new_camera_mtx)

        if not ret:
            continue

        cv2.imshow("raw_img", cv2.resize(frame, (256*3, 144*3)))
        cv2.imshow('un_distort_img', cv2.resize(dst, (256*3, 144*3)))

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()






