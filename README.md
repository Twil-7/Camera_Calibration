# Camera_Calibration

摄像头的畸变会让人们看到的图像出现“拉伸”或“扭曲”的直观感受，出现“横不平，竖不直”的现象。虽然畸变现象改变了图像原有的面貌，但在日常生活中也有很多应用之处，比如转弯路口的凸透镜，汽车的左右后视镜等，利用畸变效果扩大视野。但在利用图像进行测量或者识别时，为了保证精度，在这种场景下，就需要尽量还原图像，也就是所说的“畸变矫正”。

# 摄像头参数：

1、相机矩阵：包括焦距（fx，fy），光学中心（Cx，Cy），完全取决于相机本身，是相机的固有属性，只需要计算一次，可用矩阵表示如下：[fx, 0, Cx; 0, fy, cy; 0, 0, 1]。

2、畸变系数：畸变数学模型的5个参数 D = （k1，k2， P1， P2， k3）。

3、相机内参：相机矩阵和畸变系数统称为相机内参，在不考虑畸变的时候，相机矩阵也会被称为相机内参。

4、相机外参：通过旋转和平移变换将3D的坐标转换为相机2维的坐标，其中的旋转矩阵和平移矩阵就被称为相机的外参；描述的是将世界坐标系转换成相机坐标系的过程。

# 先验知识：

f_x, f_y are the x and y focal lengths ( yes, they are usually the same ).

In other words, you need to know the focal length of the camera, the optical center in the image and the radial distortion parameters. So you need to calibrate your camera. Of course, for the lazy dudes and dudettes among us, this is too much work. Can I supply a hack ? Of course, I can! We are already in approximation land by not using an accurate 3D model.

We can approximate the optical center by the center of the image, approximate the focal length by the width of the image in pixels and assume that radial distortion does not exist.

focal_length = size[1]    

center = [size[1]/2, size[0]/2]   

camera_matrix = np.array([[focal_length, 0, center[0]], [0, focal_length, center[1]], [0, 0, 1]])

fx和fy可以用图像的宽来近似，cx、cy分别用图像的长/2、宽/2来近似。借助这些先验知识，可以判断矫正结果的准确性。

# 运行：

提供了python和c++版本的代码，python版本直接运行calc_undistort.py即可，c++版本直接运行cameraCalibrationWithUndistortion.cpp即可。


