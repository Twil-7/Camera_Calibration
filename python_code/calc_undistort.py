#!/usr/bin/env python

import cv2
import numpy as np
import os
import glob


# 棋盘格尺寸(6, 4)，上下含6个格子内点，左右含4个格子内点
CHECKERBOARD = (6, 4)

# 迭代终止条件：迭代30次或最大误差容限0.001
# cv2.TERM_CRITERIA_EPS ： 2
# cv2.TERM_CRITERIA_MAX_ITER ： 1
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# coordinate_3d : store 3D points coordination for each checkerboard
# coordinate_2d : store 2D points coordination for each checkerboard
coordinate_3d = []
coordinate_2d = []

# 由于世界坐标系可随意定义，故可将棋盘格索引坐标，作为棋盘格3d空间坐标
index_3d = np.zeros((1, CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
index_3d[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

images = glob.glob('./raw_img/*.jpg')
images.sort()
size = cv2.imread(images[0]).shape    # 每张rgb图片尺寸：(1440, 2560, 3)

for name in images:

    img = cv2.imread(name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print('Detect img : ', name)

    # Find the chessboard corners coordinate
    ret, corners = cv2.findChessboardCorners(
        gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH+cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)

    if ret:

        # refine the pixel coordinates
        better_corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        coordinate_3d.append(index_3d)
        coordinate_2d.append(better_corners)

        # Draw and display the corners
    #     img = cv2.drawChessboardCorners(img, CHECKERBOARD, better_corners, ret)
    #
    # cv2.imshow('img', cv2.resize(img, (256*3, 144*3)))
    # cv2.waitKey(0)

# cv2.destroyAllWindows()

# mtx   : 相机内参矩阵
# dist  : 畸变系数
# r_vec : 外参旋转矩阵
# t_vec : 外参平移向量

ret, mtx, dist, r_vec, t_vec = cv2.calibrateCamera(coordinate_3d, coordinate_2d, (size[1], size[0]), None, None)
print("Camera matrix : \n")
print(mtx)
print("distortion : \n")
print(dist)


# 主要函数介绍：
# 1、cv2.findChessboardCorners函数 ： 检测棋盘格内点的2d坐标
# 2、cv2.cornerSubPix函数 ： 进一步优化棋盘格内点2d坐标的检测效果
# 3、cv2.calibrateCamera函数 ： 根据空间3d坐标和像素2d坐标，计算出相机内参和外参数值
# 4、cv2.getOptimalNewCameraMatrix函数 ： 将畸变参数与内参矩阵融合，得到含畸变的内参矩阵
# 5、cv2.undistort函数 ： 对畸变图片进行矫正，还原出无畸变图片

# 最终运算结果：
# mtx = np.array([[8.45559259e+02, 0.00000000e+00, 1.32460030e+03],
#                 [0.00000000e+00, 8.50592806e+02, 7.29938055e+02],
#                 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
# dist = np.array([[-1.12961572e-01, 1.54572487e-02, -1.66183578e-03, -1.09252844e-04, -1.15994476e-03]])

# 对于相机内参矩阵：[[fx, 0, cx], [0, fy, cy], [0, 0, 1]
# 一般都可近似 fx = fy = size[1], cx = size[1]/2, cy = size[0]/2
