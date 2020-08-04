cmake_minimum_required(VERSION 3.10)
project(example)

find_library(TENSORFLOW_LIB tensorflow HINT $ENV{HOME}/libtensorflow/lib)
find_path(CPPFLOW_PATH cppflow PATHS /usr/local/include /usr/include)

set(CMAKE_CXX_STANDARD 17)
add_executable(example test.cpp ${CPPFLOW_PATH}/cppflow/src/Model.cpp ${CPPFLOW_PATH}/cppflow/src/Tensor.cpp)
#target_include_directories(example PRIVATE ${CPPFLOW_PATH})
target_include_directories(example PUBLIC $<INSTALL_INTERFACE:include/cppflow>)
target_link_libraries (example "${TENSORFLOW_LIB}")
