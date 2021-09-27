#include <opencv2/opencv.hpp>
#include <opencv2/calib3d/calib3d.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <stdio.h>
#include <iostream>

// 此棋盘格图片：从上到下有6个内点，从左到右有9个内点
int CHECKERBOARD[2]{6,9}; 

int main()
{
  // objpoints中每个元素都是一个小vector，每个小vector存储的每个元素都是opencv的cv::Point3f数据结构
  // n * 54 * 3 * 1
  std::vector<std::vector<cv::Point3f>> objpoints;

  // imgpoints中每个元素都是一个小vector，每个小vector存储的每个元素都是opencv的cv::Point2f数据结构
  // n * 54 * 2 * 1
  std::vector<std::vector<cv::Point2f>> imgpoints;

  // objp : 54 * 3 * 1, 记录单张棋盘格，54个内点的3d位置索引
  // 指定棋盘格坐标点时，按照先从上到下，后从左到右的顺序记录。每一行棋盘格的记录方式：(y索引, x索引， 0）
  //  [0, 0, 0;
  //  1, 0, 0;
  //  2, 0, 0;
  //  3, 0, 0;
  //  ... ...
  //  2, 8, 0;
  //  3, 8, 0;
  //  4, 8, 0;
  //  5, 8, 0]

  std::vector<cv::Point3f> objp;
  for(int i{0}; i<CHECKERBOARD[1]; i++)
  {
    for(int j{0}; j<CHECKERBOARD[0]; j++)
      objp.push_back(cv::Point3f(j,i,0));
  }

  // images : 所有棋盘格图片的存储路径
  std::vector<cv::String> images;
  std::string path = "./images/*.jpg";
  cv::glob(path, images);
  
  cv::Mat frame, gray;

  // corner_pts ： 记录检测到的棋盘格54个内点的2D像素坐标
  std::vector<cv::Point2f> corner_pts;
  bool success;

  for(int i{0}; i<images.size(); i++)
  {
    // 图像大小：[640 x 480]
    frame = cv::imread(images[i]); 

    cv::cvtColor(frame, gray, cv::COLOR_BGR2GRAY);
     

    // cv::Size(CHECKERBOARD[0],CHECKERBOARD[1]) ： [6 x 9]
    // cv::CALIB_CB_ADAPTIVE_THRESH ： 1
    // cv::CALIB_CB_FAST_CHECK      ： 8
    // cv::CALIB_CB_NORMALIZE_IMAGE ： 2
    success = cv::findChessboardCorners(gray,cv::Size(CHECKERBOARD[0],CHECKERBOARD[1]), corner_pts, cv::CALIB_CB_ADAPTIVE_THRESH | cv::CALIB_CB_FAST_CHECK | cv::CALIB_CB_NORMALIZE_IMAGE);


    if(success)
    { 

      // cv::TermCriteria::EPS ： 2 
      // cv::TermCriteria::MAX_ITER ： 1
      cv::TermCriteria criteria(cv::TermCriteria::EPS | cv::TermCriteria::MAX_ITER, 30, 0.001);


      // 进一步refine检测到的网格内点的坐标精度
      // 这里cornerSubPix函数直接在原有corner_pts基础上进行覆盖，不会多创建一个新的变量再赋值
      cv::cornerSubPix(gray, corner_pts, cv::Size(11,11), cv::Size(-1,-1), criteria);
      

      // 作图
      cv::drawChessboardCorners(frame, cv::Size(CHECKERBOARD[0],CHECKERBOARD[1]), corner_pts, success);

      objpoints.push_back(objp);
      imgpoints.push_back(corner_pts);

    }

    cv::imshow("Image",frame);
    cv::waitKey(0);
  }

  cv::destroyAllWindows();

  cv::Mat cameraMatrix, distCoeffs, R, T;

  cv::calibrateCamera(objpoints, imgpoints, cv::Size(gray.rows,gray.cols), cameraMatrix,distCoeffs,R,T);

  std::cout << "cameraMatrix : " << cameraMatrix << std::endl;
  std::cout << "distCoeffs : " << distCoeffs << std::endl;
  std::cout << "Rotation vector : " << R << std::endl;
  std::cout << "Translation vector : " << T << std::endl;


  // 根据计算得到的内参、畸变系数，对畸变图片进行矫正
  cv::Mat image;
  image = cv::imread(images[0]);
  cv::Mat dst, map1, map2,new_camera_matrix;
  cv::Size imageSize(cv::Size(image.cols, image.rows));

  // Refining the camera matrix using parameters obtained by calibration
  new_camera_matrix = cv::getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, imageSize, 1, imageSize, 0);

  // Method 1 to undistort the image
  cv::undistort(frame, dst, new_camera_matrix, distCoeffs, new_camera_matrix );

  // Method 2 to undistort the image
  cv::initUndistortRectifyMap(cameraMatrix, distCoeffs, cv::Mat(),cv::getOptimalNewCameraMatrix(cameraMatrix, distCoeffs,   imageSize, 1, imageSize, 0),imageSize, CV_16SC2, map1, map2);

  cv::remap(frame, dst, map1, map2, cv::INTER_LINEAR);

  cv::imshow("undistorted image",dst);
  cv::waitKey(0);

  return 0;
}
