cmake_minimum_required(VERSION 3.12)
project(FocSampl)

set(CMAKE_CXX_STANDARD 14)

# Set output as OUT OF SOURCE
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)


IF(CMAKE_BUILD_TYPE MATCHES Release)
    add_definitions("-O2")
    add_definitions("-flto")
ELSE(CMAKE_BUILD_TYPE MATCHES Release)
    # Whatever DEBUG flags you need
    add_definitions("-g")
ENDIF(CMAKE_BUILD_TYPE MATCHES Release)

# Usually you do it like this, with specific source and include directories
# file(GLOB_RECURSE SRC_FILES_C ${PROJECT_SOURCE_DIR}/*.c)
# file(GLOB_RECURSE SRC_FILES_H ${PROJECT_SOURCE_DIR}/*.h)
# file(GLOB_RECURSE SRC_FILES_CC ${PROJECT_SOURCE_DIR}/*.cc)
# file(GLOB_RECURSE SRC_FILES_HH ${PROJECT_SOURCE_DIR}/*.hh)

list( APPEND SRCS RelationCol.cc relspec.cc  infra/cmeasure.c infra/GenRandIntVec.cc )
list( APPEND INCS RelationCol.hh relspec.hh  infra/cmeasure.h infra/GenRandIntVec.hh )

add_library(rel_lib STATIC ${SRCS} ${INCS})

add_executable(focusedSampling main.cc ${INCS})

target_link_libraries(focusedSampling LINK_PUBLIC rel_lib)

