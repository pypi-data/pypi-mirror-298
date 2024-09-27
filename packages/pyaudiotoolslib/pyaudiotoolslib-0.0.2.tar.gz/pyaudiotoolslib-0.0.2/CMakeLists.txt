cmake_minimum_required(VERSION 3.27)
project(AudioToolsLib)

set(CMAKE_CXX_STANDARD 17)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)  # -fPIC

if (MSVC)
    set(CMAKE_CXX_FLAGS_RELEASE "/O2 /Ob2 /DNDEBUG /EHsc /GL")

    # Фикс ошибок сборки
    set(HAVE_GETTIMEOFDAY 0)
else ()
    set(CMAKE_CXX_FLAGS_RELEASE "-O2 -DNDEBUG")
endif ()

include(FetchContent)

if(NOT SKBUILD_STATE STREQUAL "sdist"
        AND EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/lib/libsndfile/CMakeLists.txt")
    message(STATUS "Using integrated libsndfile")
    add_subdirectory(lib/libsndfile)
else()
    FetchContent_Declare(
            libsndfile
            GIT_REPOSITORY https://github.com/libsndfile/libsndfile.git
            GIT_TAG 1.2.2
            SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/lib/libsndfile)
    FetchContent_MakeAvailable(libsndfile)
endif()


set(
        SOURCES
        src/effects/ClickRemoval.h
        src/effects/ClickRemoval.cpp
        src/effects/audacity_mock.h
        src/effects/audacity_mock.cpp
        src/effects.h
        src/effects.cpp
        src/effects/Normalize.cpp
        src/effects/Normalize.h
        src/AudioFile.cpp
        src/AudioFile.h
        src/utils.h
)

add_executable(${PROJECT_NAME} ${SOURCES} main.cpp)

target_link_libraries(${PROJECT_NAME} PRIVATE sndfile) # OpenMP::OpenMP_CXX

# Добавляем поддержку библиотеки OpenMP
#if (NOT MSVC)
#find_package(OpenMP REQUIRED)
#if (NOT OpenMP_CXX_FOUND)
#    message(SEND_ERROR "Failed to find OpenMP.")
#    return()
#else ()
#    include_directories(${OpenMP_INCLUDE_DIRS})
#    message(STATUS "OpenMP FOUND dir is ${OpenMP_INCLUDE_DIRS}.")
#endif ()
## Дополнительный флаг, необходим для функционирования библиотеки
#if (MSVC)
#    set(CMAKE_CXX_FLAGS "/openmp:llvm")
#else ()
#    set(CMAKE_CXX_FLAGS "-fopenmp")
#endif ()


# ---------------------------- Биндинги для питона ---------------------------- #

if (NOT SKBUILD_PROJECT_NAME)
    set(PYTHON_PACKAGE pyaudiotoolslib)
else ()
    set(PYTHON_PACKAGE ${SKBUILD_PROJECT_NAME})
endif ()

set(PYBIND11_FINDPYTHON ON)
if(NOT SKBUILD_STATE STREQUAL "sdist"
        AND EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/lib/pybind11/CMakeLists.txt")
    message(STATUS "Using integrated pybind11")
    add_subdirectory(lib/pybind11)
else()
    FetchContent_Declare(
            pybind11
            GIT_REPOSITORY https://github.com/pybind/pybind11.git
            GIT_TAG v2.13.6
            SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/lib/pybind11)
    FetchContent_MakeAvailable(pybind11)
endif()

set(
        PYTHON_SOURCES
        src/python_bindings.cpp
)

set(PYTHON_MODULES wavfile utils)

foreach (PYTHON_MODULE ${PYTHON_MODULES})
    pybind11_add_module(${PYTHON_MODULE} MODULE ${PYTHON_SOURCES} ${SOURCES})
    target_link_libraries(${PYTHON_MODULE} PRIVATE sndfile) # OpenMP::OpenMP_CXX
    install(TARGETS ${PYTHON_MODULE} LIBRARY DESTINATION pyaudiotoolslib COMPONENT pylib)
endforeach ()

get_property(install_components GLOBAL PROPERTY COMPONENTS)
message(STATUS "Install components available: ${install_components}")
