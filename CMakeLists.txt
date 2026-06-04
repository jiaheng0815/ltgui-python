cmake_minimum_required(VERSION 3.18)
project(ltgui_python LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# ---- Find Python and pybind11 ----
set(PYBIND11_FINDPYTHON ON)
find_package(Python COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 REQUIRED)

# ---- Paths to ltgui C++ library ----
if(NOT DEFINED LTGUI_ROOT)
    if(DEFINED ENV{LTGUI_ROOT})
        set(LTGUI_ROOT "$ENV{LTGUI_ROOT}")
    else()
        set(LTGUI_ROOT "${CMAKE_SOURCE_DIR}/../ltgui")
    endif()
endif()
message(STATUS "LTGUI_ROOT = ${LTGUI_ROOT}")

set(LTGUI_INCLUDE_DIR "${LTGUI_ROOT}/include")
set(LTGUI_VENDOR_DIR "${LTGUI_ROOT}/vendor")

# ---- Static library name varies by platform ----
if(WIN32)
    set(LTGUI_LIB "${LTGUI_ROOT}/build/lib/ltgui.lib")
elseif(APPLE)
    set(LTGUI_LIB "${LTGUI_ROOT}/build/lib/libltgui.a")
else()
    set(LTGUI_LIB "${LTGUI_ROOT}/build/lib/libltgui.a")
endif()

# ---- The binding module ----
pybind11_add_module(_ltgui src/_ltgui.cpp)

target_include_directories(_ltgui PRIVATE
    ${LTGUI_INCLUDE_DIR}
    ${LTGUI_INCLUDE_DIR}/ltgui
    ${LTGUI_VENDOR_DIR}
)

target_link_libraries(_ltgui PRIVATE ${LTGUI_LIB})

# ---- Platform-specific libraries ----
if(WIN32)
    target_compile_definitions(_ltgui PRIVATE
        _UNICODE UNICODE NOMINMAX
    )
    target_link_libraries(_ltgui PRIVATE
        gdi32 gdiplus user32 comctl32 ole32 imm32
        d3d11 dxgi d3dcompiler
    )
    target_link_options(_ltgui PRIVATE -static)
elseif(APPLE)
    target_compile_definitions(_ltgui PRIVATE LTGUI_PLATFORM_MACOS)
    target_link_libraries(_ltgui PRIVATE
        "-framework Cocoa"
        "-framework CoreGraphics"
        "-framework CoreText"
    )
else()
    target_compile_definitions(_ltgui PRIVATE LTGUI_PLATFORM_LINUX)
    target_link_libraries(_ltgui PRIVATE
        X11 Xft Xrender fontconfig EGL GLESv2
    )
    find_package(Freetype)
    if(FREETYPE_FOUND)
        target_include_directories(_ltgui PRIVATE ${FREETYPE_INCLUDE_DIRS})
        target_link_libraries(_ltgui PRIVATE ${FREETYPE_LIBRARIES})
    endif()
endif()

# Copy output .pyd/.so to ltgui/ package directory
add_custom_command(TARGET _ltgui POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "$<TARGET_FILE:_ltgui>"
        "${CMAKE_SOURCE_DIR}/ltgui/"
)
