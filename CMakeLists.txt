cmake_minimum_required(VERSION 3.18)

set(CMAKE_CXX_STANDARD 14)

project(sample)

if (NOT EXISTS "${CMAKE_BINARY_DIR}/conan.cmake")
    message(STATUS "Downloading conan.cmake from https://github.com/conan-io/cmake-conan")
    file(DOWNLOAD "https://raw.githubusercontent.com/conan-io/cmake-conan/master/conan.cmake" "${CMAKE_BINARY_DIR}/conan.cmake")
endif ()
include(${CMAKE_BINARY_DIR}/conan.cmake)

if (CONAN_PROFILE_BUILD AND CONAN_PROFILE_HOST)
    conan_cmake_install(PATH_OR_REFERENCE ${CMAKE_CURRENT_LIST_DIR} BUILD missing
        SETTINGS_HOST build_type=${CMAKE_BUILD_TYPE}
        SETTINGS_BUILD build_type=${CMAKE_BUILD_TYPE}
        PROFILE_BUILD ${CONAN_PROFILE_BUILD}
        PROFILE_HOST ${CONAN_PROFILE_HOST})
else ()
    conan_cmake_autodetect(settings)
    conan_cmake_install(PATH_OR_REFERENCE ${CMAKE_CURRENT_LIST_DIR} BUILD missing SETTINGS ${settings})
endif ()

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(${PROJECT_NAME} main.cc)

if (IOS)
    set_target_properties(${PROJECT_NAME} PROPERTIES
        LINK_FLAGS "-Wl,-rpath,@loader_path/Frameworks"     # for iOS iPhone Debug
        MACOSX_BUNDLE_GUI_IDENTIFIER com.netease.nmc.sample # bundle ID
        MACOSX_BUNDLE_BUNDLE_VERSION 1.0                    # version
        MACOSX_BUNDLE_SHORT_VERSION_STRING 1.0.0            # short version
        XCODE_ATTRIBUTE_ENABLE_BITCODE ON                   # enabled bitcode
        XCODE_ATTRIBUTE_OTHER_CODE_SIGN_FLAGS "--deep"      # codesign --deep
    )
endif ()

target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS})
