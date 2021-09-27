#!/usr/bin/env python

import cv2
import numpy as np
import os
import glob


images = glob.glob('./raw_img/*.jpg')
images.sort()
size = cv2.imread(images[0]).shape    # (1440, 2560, 3)
h, w = size[:2]

mtx = np.array([[8.45559259e+02, 0.00000000e+00, 1.32460030e+03],
                [0.00000000e+00, 8.50592806e+02, 7.29938055e+02],
                [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
dist = np.array([[-1.12961572e-01, 1.54572487e-02, -1.66183578e-03, -1.09252844e-04, -1.15994476e-03]])


for name in images:

    img = cv2.imread(name)

    # new_camera_mtx : 将畸变系数与相机内参矩阵融合，得到带畸变的内参矩阵
    new_camera_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 0.2, (w, h))
    adjust_img = cv2.undistort(img, mtx, dist, None, new_camera_mtx)

    name1 = name.split('/')
    name2 = name1[2]
    cv2.imwrite("adjust_img/" + name2, adjust_img)
