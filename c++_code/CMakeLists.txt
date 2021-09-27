cmake_minimum_required(VERSION 2.8.12)

set(CMAKE_CXX_STANDARD 14)

# 将该工程命名为：cameracalib
PROJECT(cameracalib)

# 寻找opencv第三方库的头文件位置、库文件位置以及库文件名称
find_package(OpenCV REQUIRED)

# 将opencv指定目录添加到编译器的头文件搜索路径之下
include_directories(${OpenCV_INCLUDE_DIRS})

MACRO(add_example name)

  # 根据源代码cameraCalibration.cpp，生成可执行文件cameraCalibration
  # 根据源代码cameraCalibrationWithUndistortion.cpp，生成可执行文件cameraCalibrationWithUndistortion

  ADD_EXECUTABLE(${name} ${name}.cpp)
  TARGET_LINK_LIBRARIES(${name} ${OpenCV_LIBS})
  
ENDMACRO()

add_example(cameraCalibration)
add_example(cameraCalibrationWithUndistortion)
