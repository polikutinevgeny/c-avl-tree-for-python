cmake_minimum_required(VERSION 3.6)
project(c_avl_tree_for_python)

set(CMAKE_CXX_STANDARD 14)

set(SOURCE_FILES
    linear_sequence_assoc.c
    linear_sequence_assoc.h)

add_library(c_avl_tree_for_python SHARED ${SOURCE_FILES})