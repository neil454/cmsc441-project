cmake_minimum_required(VERSION 3.2.2) # CMake version check
project(project2)               # Create project "simple_example"
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11") # Enable c++11 standard

find_package(OpenMP)
if (OPENMP_FOUND)
    set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
endif()

set(SOURCE_FILES project2.cpp)            # Add main.cpp file of project root directory as source file
add_executable(project2 ${SOURCE_FILES})       # Add executable target with source files listed in SOURCE_FILES variable