########## MACROS ###########################################################################
#############################################################################################

function(conan_message MESSAGE_OUTPUT)
    if(NOT CONAN_CMAKE_SILENT_OUTPUT)
        message(${ARGV${0}})
    endif()
endfunction()


macro(conan_find_apple_frameworks FRAMEWORKS_FOUND FRAMEWORKS FRAMEWORKS_DIRS)
    if(APPLE)
        foreach(_FRAMEWORK ${FRAMEWORKS})
            # https://cmake.org/pipermail/cmake-developers/2017-August/030199.html
            find_library(CONAN_FRAMEWORK_${_FRAMEWORK}_FOUND NAMES ${_FRAMEWORK} PATHS ${FRAMEWORKS_DIRS} CMAKE_FIND_ROOT_PATH_BOTH)
            if(CONAN_FRAMEWORK_${_FRAMEWORK}_FOUND)
                list(APPEND ${FRAMEWORKS_FOUND} ${CONAN_FRAMEWORK_${_FRAMEWORK}_FOUND})
            else()
                message(FATAL_ERROR "Framework library ${_FRAMEWORK} not found in paths: ${FRAMEWORKS_DIRS}")
            endif()
        endforeach()
    endif()
endmacro()


function(conan_package_library_targets libraries package_libdir deps out_libraries out_libraries_target build_type package_name)
    unset(_CONAN_ACTUAL_TARGETS CACHE)
    unset(_CONAN_FOUND_SYSTEM_LIBS CACHE)
    foreach(_LIBRARY_NAME ${libraries})
        find_library(CONAN_FOUND_LIBRARY NAMES ${_LIBRARY_NAME} PATHS ${package_libdir}
                     NO_DEFAULT_PATH NO_CMAKE_FIND_ROOT_PATH)
        if(CONAN_FOUND_LIBRARY)
            conan_message(STATUS "Library ${_LIBRARY_NAME} found ${CONAN_FOUND_LIBRARY}")
            list(APPEND _out_libraries ${CONAN_FOUND_LIBRARY})
            if(NOT ${CMAKE_VERSION} VERSION_LESS "3.0")
                # Create a micro-target for each lib/a found
                string(REGEX REPLACE "[^A-Za-z0-9.+_-]" "_" _LIBRARY_NAME ${_LIBRARY_NAME})
                set(_LIB_NAME CONAN_LIB::${package_name}_${_LIBRARY_NAME}${build_type})
                if(NOT TARGET ${_LIB_NAME})
                    # Create a micro-target for each lib/a found
                    add_library(${_LIB_NAME} UNKNOWN IMPORTED)
                    set_target_properties(${_LIB_NAME} PROPERTIES IMPORTED_LOCATION ${CONAN_FOUND_LIBRARY})
                    set(_CONAN_ACTUAL_TARGETS ${_CONAN_ACTUAL_TARGETS} ${_LIB_NAME})
                else()
                    conan_message(STATUS "Skipping already existing target: ${_LIB_NAME}")
                endif()
                list(APPEND _out_libraries_target ${_LIB_NAME})
            endif()
            conan_message(STATUS "Found: ${CONAN_FOUND_LIBRARY}")
        else()
            conan_message(STATUS "Library ${_LIBRARY_NAME} not found in package, might be system one")
            list(APPEND _out_libraries_target ${_LIBRARY_NAME})
            list(APPEND _out_libraries ${_LIBRARY_NAME})
            set(_CONAN_FOUND_SYSTEM_LIBS "${_CONAN_FOUND_SYSTEM_LIBS};${_LIBRARY_NAME}")
        endif()
        unset(CONAN_FOUND_LIBRARY CACHE)
    endforeach()

    if(NOT ${CMAKE_VERSION} VERSION_LESS "3.0")
        # Add all dependencies to all targets
        string(REPLACE " " ";" deps_list "${deps}")
        foreach(_CONAN_ACTUAL_TARGET ${_CONAN_ACTUAL_TARGETS})
            set_property(TARGET ${_CONAN_ACTUAL_TARGET} PROPERTY INTERFACE_LINK_LIBRARIES "${_CONAN_FOUND_SYSTEM_LIBS};${deps_list}")
        endforeach()
    endif()

    set(${out_libraries} ${_out_libraries} PARENT_SCOPE)
    set(${out_libraries_target} ${_out_libraries_target} PARENT_SCOPE)
endfunction()


########### FOUND PACKAGE ###################################################################
#############################################################################################

include(FindPackageHandleStandardArgs)

conan_message(STATUS "Conan: Using autogenerated FindGTest.cmake")
set(GTest_FOUND 1)
set(GTest_VERSION "1.10.0")

find_package_handle_standard_args(GTest REQUIRED_VARS
                                  GTest_VERSION VERSION_VAR GTest_VERSION)
mark_as_advanced(GTest_FOUND GTest_VERSION)

set(GTest_COMPONENTS GTest::gtest_main GTest::gmock_main GTest::gmock GTest::gtest)

if(GTest_FIND_COMPONENTS)
    foreach(_FIND_COMPONENT ${GTest_FIND_COMPONENTS})
        list(FIND GTest_COMPONENTS "GTest::${_FIND_COMPONENT}" _index)
        if(${_index} EQUAL -1)
            conan_message(FATAL_ERROR "Conan: Component '${_FIND_COMPONENT}' NOT found in package 'GTest'")
        else()
            conan_message(STATUS "Conan: Component '${_FIND_COMPONENT}' found in package 'GTest'")
        endif()
    endforeach()
endif()

########### VARIABLES #######################################################################
#############################################################################################


set(GTest_INCLUDE_DIRS "C:/Users/Quarter/.conan/data/gtest/1.10.0/_/_/package/111c650f4a6662c61f14f93de06e27092d1db0ae/include")
set(GTest_INCLUDE_DIR "C:/Users/Quarter/.conan/data/gtest/1.10.0/_/_/package/111c650f4a6662c61f14f93de06e27092d1db0ae/include")
set(GTest_INCLUDES "C:/Users/Quarter/.conan/data/gtest/1.10.0/_/_/package/111c650f4a6662c61f14f93de06e27092d1db0ae/include")
set(GTest_RES_DIRS )
set(GTest_DEFINITIONS )
set(GTest_LINKER_FLAGS_LIST
        "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,SHARED_LIBRARY>:>"
        "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,MODULE_LIBRARY>:>"
        "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,EXECUTABLE>:>"
)
set(GTest_COMPILE_DEFINITIONS )
set(GTest_COMPILE_OPTIONS_LIST "" "")
set(GTest_COMPILE_OPTIONS_C "")
set(GTest_COMPILE_OPTIONS_CXX "")
set(GTest_LIBRARIES_TARGETS "") # Will be filled later, if CMake 3
set(GTest_LIBRARIES "") # Will be filled later
set(GTest_LIBS "") # Same as GTest_LIBRARIES
set(GTest_SYSTEM_LIBS )
set(GTest_FRAMEWORK_DIRS )
set(GTest_FRAMEWORKS )
set(GTest_FRAMEWORKS_FOUND "") # Will be filled later
set(GTest_BUILD_MODULES_PATHS )

conan_find_apple_frameworks(GTest_FRAMEWORKS_FOUND "${GTest_FRAMEWORKS}" "${GTest_FRAMEWORK_DIRS}")

mark_as_advanced(GTest_INCLUDE_DIRS
                 GTest_INCLUDE_DIR
                 GTest_INCLUDES
                 GTest_DEFINITIONS
                 GTest_LINKER_FLAGS_LIST
                 GTest_COMPILE_DEFINITIONS
                 GTest_COMPILE_OPTIONS_LIST
                 GTest_LIBRARIES
                 GTest_LIBS
                 GTest_LIBRARIES_TARGETS)

# Find the real .lib/.a and add them to GTest_LIBS and GTest_LIBRARY_LIST
set(GTest_LIBRARY_LIST gtest_main gmock_main gmock gtest)
set(GTest_LIB_DIRS "C:/Users/Quarter/.conan/data/gtest/1.10.0/_/_/package/111c650f4a6662c61f14f93de06e27092d1db0ae/lib")

# Gather all the libraries that should be linked to the targets (do not touch existing variables):
set(_GTest_DEPENDENCIES "${GTest_FRAMEWORKS_FOUND} ${GTest_SYSTEM_LIBS} ")

conan_package_library_targets("${GTest_LIBRARY_LIST}"  # libraries
                              "${GTest_LIB_DIRS}"      # package_libdir
                              "${_GTest_DEPENDENCIES}"  # deps
                              GTest_LIBRARIES            # out_libraries
                              GTest_LIBRARIES_TARGETS    # out_libraries_targets
                              ""                          # build_type
                              "GTest")                                      # package_name

set(GTest_LIBS ${GTest_LIBRARIES})

foreach(_FRAMEWORK ${GTest_FRAMEWORKS_FOUND})
    list(APPEND GTest_LIBRARIES_TARGETS ${_FRAMEWORK})
    list(APPEND GTest_LIBRARIES ${_FRAMEWORK})
endforeach()

foreach(_SYSTEM_LIB ${GTest_SYSTEM_LIBS})
    list(APPEND GTest_LIBRARIES_TARGETS ${_SYSTEM_LIB})
    list(APPEND GTest_LIBRARIES ${_SYSTEM_LIB})
endforeach()

# We need to add our requirements too
set(GTest_LIBRARIES_TARGETS "${GTest_LIBRARIES_TARGETS};")
set(GTest_LIBRARIES "${GTest_LIBRARIES};")

set(CMAKE_MODULE_PATH  ${CMAKE_MODULE_PATH})
set(CMAKE_PREFIX_PATH  ${CMAKE_PREFIX_PATH})


########### COMPONENT gtest VARIABLES #############################################

set(GTest_gtest_INCLUDE_DIRS "C:/Users/Quarter/.conan/data/gtest/1.10.0/_/_/package/111c650f4a6662c61f14f93de06e27092d1db0ae/include")
set(GTest_gtest_INCLUDE_DIR "C:/Users/Quarter/.conan/data/gtest/1.10.0/_/_/package/111c650f4a6662c61f14f93de06e27092d1db0ae/include")
set(GTest_gtest_INCLUDES "C:/Users/Quarter/.conan/data/gtest/1.10.0/_/_/package/111c650f4a6662c61f14f93de06e27092d1db0ae/include")
set(GTest_gtest_LIB_DIRS "C:/Users/Quarter/.conan/data/gtest/1.10.0/_/_/package/111c650f4a6662c61f14f93de06e27092d1db0ae/lib")
set(GTest_gtest_RES_DIRS )
set(GTest_gtest_DEFINITIONS )
set(GTest_gtest_COMPILE_DEFINITIONS )
set(GTest_gtest_COMPILE_OPTIONS_C "")
set(GTest_gtest_COMPILE_OPTIONS_CXX "")
set(GTest_gtest_LIBS gtest)
set(GTest_gtest_SYSTEM_LIBS )
set(GTest_gtest_FRAMEWORK_DIRS )
set(GTest_gtest_FRAMEWORKS )
set(GTest_gtest_BUILD_MODULES_PATHS )
set(GTest_gtest_DEPENDENCIES )
set(GTest_gtest_LINKER_FLAGS_LIST
        "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,SHARED_LIBRARY>:>"
        "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,MODULE_LIBRARY>:>"
        "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,EXECUTABLE>:>"
)

########### COMPONENT gmock VARIABLES #############################################

set(GTest_gmock_INCLUDE_DIRS "C:/Users/Quarter/.conan/data/gtest/1.10.0/_/_/package/111c650f4a6662c61f14f93de06e27092d1db0ae/include")
set(GTest_gmock_INCLUDE_DIR "C:/Users/Quarter/.conan/data/gtest/1.10.0/_/_/package/111c650f4a6662c61f14f93de06e27092d1db0ae/include")
set(GTest_gmock_INCLUDES "C:/Users/Quarter/.conan/data/gtest/1.10.0/_/_/package/111c650f4a6662c61f14f93de06e27092d1db0ae/include")
set(GTest_gmock_LIB_DIRS "C:/Users/Quarter/.conan/data/gtest/1.10.0/_/_/package/111c650f4a6662c61f14f93de06e27092d1db0ae/lib")
set(GTest_gmock_RES_DIRS )
set(GTest_gmock_DEFINITIONS )
set(GTest_gmock_COMPILE_DEFINITIONS )
set(GTest_gmock_COMPILE_OPTIONS_C "")
set(GTest_gmock_COMPILE_OPTIONS_CXX "")
set(GTest_gmock_LIBS gmock)
set(GTest_gmock_SYSTEM_LIBS )
set(GTest_gmock_FRAMEWORK_DIRS )
set(GTest_gmock_FRAMEWORKS )
set(GTest_gmock_BUILD_MODULES_PATHS )
set(GTest_gmock_DEPENDENCIES GTest::gtest)
set(GTest_gmock_LINKER_FLAGS_LIST
        "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,SHARED_LIBRARY>:>"
        "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,MODULE_LIBRARY>:>"
        "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,EXECUTABLE>:>"
)

########### COMPONENT gmock_main VARIABLES #############################################

set(GTest_gmock_main_INCLUDE_DIRS "C:/Users/Quarter/.conan/data/gtest/1.10.0/_/_/package/111c650f4a6662c61f14f93de06e27092d1db0ae/include")
set(GTest_gmock_main_INCLUDE_DIR "C:/Users/Quarter/.conan/data/gtest/1.10.0/_/_/package/111c650f4a6662c61f14f93de06e27092d1db0ae/include")
set(GTest_gmock_main_INCLUDES "C:/Users/Quarter/.conan/data/gtest/1.10.0/_/_/package/111c650f4a6662c61f14f93de06e27092d1db0ae/include")
set(GTest_gmock_main_LIB_DIRS "C:/Users/Quarter/.conan/data/gtest/1.10.0/_/_/package/111c650f4a6662c61f14f93de06e27092d1db0ae/lib")
set(GTest_gmock_main_RES_DIRS )
set(GTest_gmock_main_DEFINITIONS )
set(GTest_gmock_main_COMPILE_DEFINITIONS )
set(GTest_gmock_main_COMPILE_OPTIONS_C "")
set(GTest_gmock_main_COMPILE_OPTIONS_CXX "")
set(GTest_gmock_main_LIBS gmock_main)
set(GTest_gmock_main_SYSTEM_LIBS )
set(GTest_gmock_main_FRAMEWORK_DIRS )
set(GTest_gmock_main_FRAMEWORKS )
set(GTest_gmock_main_BUILD_MODULES_PATHS )
set(GTest_gmock_main_DEPENDENCIES GTest::gmock)
set(GTest_gmock_main_LINKER_FLAGS_LIST
        "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,SHARED_LIBRARY>:>"
        "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,MODULE_LIBRARY>:>"
        "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,EXECUTABLE>:>"
)

########### COMPONENT gtest_main VARIABLES #############################################

set(GTest_gtest_main_INCLUDE_DIRS "C:/Users/Quarter/.conan/data/gtest/1.10.0/_/_/package/111c650f4a6662c61f14f93de06e27092d1db0ae/include")
set(GTest_gtest_main_INCLUDE_DIR "C:/Users/Quarter/.conan/data/gtest/1.10.0/_/_/package/111c650f4a6662c61f14f93de06e27092d1db0ae/include")
set(GTest_gtest_main_INCLUDES "C:/Users/Quarter/.conan/data/gtest/1.10.0/_/_/package/111c650f4a6662c61f14f93de06e27092d1db0ae/include")
set(GTest_gtest_main_LIB_DIRS "C:/Users/Quarter/.conan/data/gtest/1.10.0/_/_/package/111c650f4a6662c61f14f93de06e27092d1db0ae/lib")
set(GTest_gtest_main_RES_DIRS )
set(GTest_gtest_main_DEFINITIONS )
set(GTest_gtest_main_COMPILE_DEFINITIONS )
set(GTest_gtest_main_COMPILE_OPTIONS_C "")
set(GTest_gtest_main_COMPILE_OPTIONS_CXX "")
set(GTest_gtest_main_LIBS gtest_main)
set(GTest_gtest_main_SYSTEM_LIBS )
set(GTest_gtest_main_FRAMEWORK_DIRS )
set(GTest_gtest_main_FRAMEWORKS )
set(GTest_gtest_main_BUILD_MODULES_PATHS )
set(GTest_gtest_main_DEPENDENCIES GTest::gtest)
set(GTest_gtest_main_LINKER_FLAGS_LIST
        "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,SHARED_LIBRARY>:>"
        "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,MODULE_LIBRARY>:>"
        "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,EXECUTABLE>:>"
)


########## FIND PACKAGE DEPENDENCY ##########################################################
#############################################################################################

include(CMakeFindDependencyMacro)


########## FIND LIBRARIES & FRAMEWORKS / DYNAMIC VARS #######################################
#############################################################################################

########## COMPONENT gtest FIND LIBRARIES & FRAMEWORKS / DYNAMIC VARS #############

set(GTest_gtest_FRAMEWORKS_FOUND "")
conan_find_apple_frameworks(GTest_gtest_FRAMEWORKS_FOUND "${GTest_gtest_FRAMEWORKS}" "${GTest_gtest_FRAMEWORK_DIRS}")

set(GTest_gtest_LIB_TARGETS "")
set(GTest_gtest_NOT_USED "")
set(GTest_gtest_LIBS_FRAMEWORKS_DEPS ${GTest_gtest_FRAMEWORKS_FOUND} ${GTest_gtest_SYSTEM_LIBS} ${GTest_gtest_DEPENDENCIES})
conan_package_library_targets("${GTest_gtest_LIBS}"
                              "${GTest_gtest_LIB_DIRS}"
                              "${GTest_gtest_LIBS_FRAMEWORKS_DEPS}"
                              GTest_gtest_NOT_USED
                              GTest_gtest_LIB_TARGETS
                              ""
                              "GTest_gtest")

set(GTest_gtest_LINK_LIBS ${GTest_gtest_LIB_TARGETS} ${GTest_gtest_LIBS_FRAMEWORKS_DEPS})

set(CMAKE_MODULE_PATH  ${CMAKE_MODULE_PATH})
set(CMAKE_PREFIX_PATH  ${CMAKE_PREFIX_PATH})

########## COMPONENT gmock FIND LIBRARIES & FRAMEWORKS / DYNAMIC VARS #############

set(GTest_gmock_FRAMEWORKS_FOUND "")
conan_find_apple_frameworks(GTest_gmock_FRAMEWORKS_FOUND "${GTest_gmock_FRAMEWORKS}" "${GTest_gmock_FRAMEWORK_DIRS}")

set(GTest_gmock_LIB_TARGETS "")
set(GTest_gmock_NOT_USED "")
set(GTest_gmock_LIBS_FRAMEWORKS_DEPS ${GTest_gmock_FRAMEWORKS_FOUND} ${GTest_gmock_SYSTEM_LIBS} ${GTest_gmock_DEPENDENCIES})
conan_package_library_targets("${GTest_gmock_LIBS}"
                              "${GTest_gmock_LIB_DIRS}"
                              "${GTest_gmock_LIBS_FRAMEWORKS_DEPS}"
                              GTest_gmock_NOT_USED
                              GTest_gmock_LIB_TARGETS
                              ""
                              "GTest_gmock")

set(GTest_gmock_LINK_LIBS ${GTest_gmock_LIB_TARGETS} ${GTest_gmock_LIBS_FRAMEWORKS_DEPS})

set(CMAKE_MODULE_PATH  ${CMAKE_MODULE_PATH})
set(CMAKE_PREFIX_PATH  ${CMAKE_PREFIX_PATH})

########## COMPONENT gmock_main FIND LIBRARIES & FRAMEWORKS / DYNAMIC VARS #############

set(GTest_gmock_main_FRAMEWORKS_FOUND "")
conan_find_apple_frameworks(GTest_gmock_main_FRAMEWORKS_FOUND "${GTest_gmock_main_FRAMEWORKS}" "${GTest_gmock_main_FRAMEWORK_DIRS}")

set(GTest_gmock_main_LIB_TARGETS "")
set(GTest_gmock_main_NOT_USED "")
set(GTest_gmock_main_LIBS_FRAMEWORKS_DEPS ${GTest_gmock_main_FRAMEWORKS_FOUND} ${GTest_gmock_main_SYSTEM_LIBS} ${GTest_gmock_main_DEPENDENCIES})
conan_package_library_targets("${GTest_gmock_main_LIBS}"
                              "${GTest_gmock_main_LIB_DIRS}"
                              "${GTest_gmock_main_LIBS_FRAMEWORKS_DEPS}"
                              GTest_gmock_main_NOT_USED
                              GTest_gmock_main_LIB_TARGETS
                              ""
                              "GTest_gmock_main")

set(GTest_gmock_main_LINK_LIBS ${GTest_gmock_main_LIB_TARGETS} ${GTest_gmock_main_LIBS_FRAMEWORKS_DEPS})

set(CMAKE_MODULE_PATH  ${CMAKE_MODULE_PATH})
set(CMAKE_PREFIX_PATH  ${CMAKE_PREFIX_PATH})

########## COMPONENT gtest_main FIND LIBRARIES & FRAMEWORKS / DYNAMIC VARS #############

set(GTest_gtest_main_FRAMEWORKS_FOUND "")
conan_find_apple_frameworks(GTest_gtest_main_FRAMEWORKS_FOUND "${GTest_gtest_main_FRAMEWORKS}" "${GTest_gtest_main_FRAMEWORK_DIRS}")

set(GTest_gtest_main_LIB_TARGETS "")
set(GTest_gtest_main_NOT_USED "")
set(GTest_gtest_main_LIBS_FRAMEWORKS_DEPS ${GTest_gtest_main_FRAMEWORKS_FOUND} ${GTest_gtest_main_SYSTEM_LIBS} ${GTest_gtest_main_DEPENDENCIES})
conan_package_library_targets("${GTest_gtest_main_LIBS}"
                              "${GTest_gtest_main_LIB_DIRS}"
                              "${GTest_gtest_main_LIBS_FRAMEWORKS_DEPS}"
                              GTest_gtest_main_NOT_USED
                              GTest_gtest_main_LIB_TARGETS
                              ""
                              "GTest_gtest_main")

set(GTest_gtest_main_LINK_LIBS ${GTest_gtest_main_LIB_TARGETS} ${GTest_gtest_main_LIBS_FRAMEWORKS_DEPS})

set(CMAKE_MODULE_PATH  ${CMAKE_MODULE_PATH})
set(CMAKE_PREFIX_PATH  ${CMAKE_PREFIX_PATH})


########## TARGETS ##########################################################################
#############################################################################################

########## COMPONENT gtest TARGET #################################################

if(NOT ${CMAKE_VERSION} VERSION_LESS "3.0")
    # Target approach
    if(NOT TARGET GTest::gtest)
        add_library(GTest::gtest INTERFACE IMPORTED)
        set_target_properties(GTest::gtest PROPERTIES INTERFACE_INCLUDE_DIRECTORIES
                              "${GTest_gtest_INCLUDE_DIRS}")
        set_target_properties(GTest::gtest PROPERTIES INTERFACE_LINK_DIRECTORIES
                              "${GTest_gtest_LIB_DIRS}")
        set_target_properties(GTest::gtest PROPERTIES INTERFACE_LINK_LIBRARIES
                              "${GTest_gtest_LINK_LIBS};${GTest_gtest_LINKER_FLAGS_LIST}")
        set_target_properties(GTest::gtest PROPERTIES INTERFACE_COMPILE_DEFINITIONS
                              "${GTest_gtest_COMPILE_DEFINITIONS}")
        set_target_properties(GTest::gtest PROPERTIES INTERFACE_COMPILE_OPTIONS
                              "${GTest_gtest_COMPILE_OPTIONS_C};${GTest_gtest_COMPILE_OPTIONS_CXX}")
    endif()
endif()

########## COMPONENT gmock TARGET #################################################

if(NOT ${CMAKE_VERSION} VERSION_LESS "3.0")
    # Target approach
    if(NOT TARGET GTest::gmock)
        add_library(GTest::gmock INTERFACE IMPORTED)
        set_target_properties(GTest::gmock PROPERTIES INTERFACE_INCLUDE_DIRECTORIES
                              "${GTest_gmock_INCLUDE_DIRS}")
        set_target_properties(GTest::gmock PROPERTIES INTERFACE_LINK_DIRECTORIES
                              "${GTest_gmock_LIB_DIRS}")
        set_target_properties(GTest::gmock PROPERTIES INTERFACE_LINK_LIBRARIES
                              "${GTest_gmock_LINK_LIBS};${GTest_gmock_LINKER_FLAGS_LIST}")
        set_target_properties(GTest::gmock PROPERTIES INTERFACE_COMPILE_DEFINITIONS
                              "${GTest_gmock_COMPILE_DEFINITIONS}")
        set_target_properties(GTest::gmock PROPERTIES INTERFACE_COMPILE_OPTIONS
                              "${GTest_gmock_COMPILE_OPTIONS_C};${GTest_gmock_COMPILE_OPTIONS_CXX}")
    endif()
endif()

########## COMPONENT gmock_main TARGET #################################################

if(NOT ${CMAKE_VERSION} VERSION_LESS "3.0")
    # Target approach
    if(NOT TARGET GTest::gmock_main)
        add_library(GTest::gmock_main INTERFACE IMPORTED)
        set_target_properties(GTest::gmock_main PROPERTIES INTERFACE_INCLUDE_DIRECTORIES
                              "${GTest_gmock_main_INCLUDE_DIRS}")
        set_target_properties(GTest::gmock_main PROPERTIES INTERFACE_LINK_DIRECTORIES
                              "${GTest_gmock_main_LIB_DIRS}")
        set_target_properties(GTest::gmock_main PROPERTIES INTERFACE_LINK_LIBRARIES
                              "${GTest_gmock_main_LINK_LIBS};${GTest_gmock_main_LINKER_FLAGS_LIST}")
        set_target_properties(GTest::gmock_main PROPERTIES INTERFACE_COMPILE_DEFINITIONS
                              "${GTest_gmock_main_COMPILE_DEFINITIONS}")
        set_target_properties(GTest::gmock_main PROPERTIES INTERFACE_COMPILE_OPTIONS
                              "${GTest_gmock_main_COMPILE_OPTIONS_C};${GTest_gmock_main_COMPILE_OPTIONS_CXX}")
    endif()
endif()

########## COMPONENT gtest_main TARGET #################################################

if(NOT ${CMAKE_VERSION} VERSION_LESS "3.0")
    # Target approach
    if(NOT TARGET GTest::gtest_main)
        add_library(GTest::gtest_main INTERFACE IMPORTED)
        set_target_properties(GTest::gtest_main PROPERTIES INTERFACE_INCLUDE_DIRECTORIES
                              "${GTest_gtest_main_INCLUDE_DIRS}")
        set_target_properties(GTest::gtest_main PROPERTIES INTERFACE_LINK_DIRECTORIES
                              "${GTest_gtest_main_LIB_DIRS}")
        set_target_properties(GTest::gtest_main PROPERTIES INTERFACE_LINK_LIBRARIES
                              "${GTest_gtest_main_LINK_LIBS};${GTest_gtest_main_LINKER_FLAGS_LIST}")
        set_target_properties(GTest::gtest_main PROPERTIES INTERFACE_COMPILE_DEFINITIONS
                              "${GTest_gtest_main_COMPILE_DEFINITIONS}")
        set_target_properties(GTest::gtest_main PROPERTIES INTERFACE_COMPILE_OPTIONS
                              "${GTest_gtest_main_COMPILE_OPTIONS_C};${GTest_gtest_main_COMPILE_OPTIONS_CXX}")
    endif()
endif()

########## GLOBAL TARGET ####################################################################

if(NOT ${CMAKE_VERSION} VERSION_LESS "3.0")
    if(NOT TARGET GTest::GTest)
        add_library(GTest::GTest INTERFACE IMPORTED)
    endif()
    set_property(TARGET GTest::GTest APPEND PROPERTY
                 INTERFACE_LINK_LIBRARIES "${GTest_COMPONENTS}")
endif()

########## BUILD MODULES ####################################################################
#############################################################################################
########## COMPONENT gtest BUILD MODULES ##########################################

foreach(_BUILD_MODULE_PATH ${GTest_gtest_BUILD_MODULES_PATHS})
    include(${_BUILD_MODULE_PATH})
endforeach()
########## COMPONENT gmock BUILD MODULES ##########################################

foreach(_BUILD_MODULE_PATH ${GTest_gmock_BUILD_MODULES_PATHS})
    include(${_BUILD_MODULE_PATH})
endforeach()
########## COMPONENT gmock_main BUILD MODULES ##########################################

foreach(_BUILD_MODULE_PATH ${GTest_gmock_main_BUILD_MODULES_PATHS})
    include(${_BUILD_MODULE_PATH})
endforeach()
########## COMPONENT gtest_main BUILD MODULES ##########################################

foreach(_BUILD_MODULE_PATH ${GTest_gtest_main_BUILD_MODULES_PATHS})
    include(${_BUILD_MODULE_PATH})
endforeach()
