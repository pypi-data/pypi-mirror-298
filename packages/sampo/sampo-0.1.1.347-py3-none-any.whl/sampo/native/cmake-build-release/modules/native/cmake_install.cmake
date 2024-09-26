# Install script for directory: C:/Users/Quarter/PycharmProjects/sampo/sampo/native/modules/native

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "C:/Users/Quarter/PycharmProjects/sampo/sampo/native/dist")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "C:/Program Files/LLVM/bin/llvm-objdump.exe")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Runtime" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "C:/Users/Quarter/PycharmProjects/sampo/sampo/native/cmake-build-release/modules/native/wheel/native/native.pyd")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "C:/Users/Quarter/PycharmProjects/sampo/sampo/native/cmake-build-release/modules/native/wheel/native" TYPE MODULE FILES "C:/Users/Quarter/PycharmProjects/sampo/sampo/native/cmake-build-release/native.pyd")
  if(EXISTS "$ENV{DESTDIR}/C:/Users/Quarter/PycharmProjects/sampo/sampo/native/cmake-build-release/modules/native/wheel/native/native.pyd" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/C:/Users/Quarter/PycharmProjects/sampo/sampo/native/cmake-build-release/modules/native/wheel/native/native.pyd")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "C:/Program Files/LLVM/bin/llvm-strip.exe" "$ENV{DESTDIR}/C:/Users/Quarter/PycharmProjects/sampo/sampo/native/cmake-build-release/modules/native/wheel/native/native.pyd")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Runtime" OR NOT CMAKE_INSTALL_COMPONENT)
  file(
    GET_RUNTIME_DEPENDENCIES
    LIBRARIES "$ENV{DESTDIR}/C:/Users/Quarter/PycharmProjects/sampo/sampo/native/cmake-build-release/modules/native/wheel/native/native.pyd"
    RESOLVED_DEPENDENCIES_VAR RESOLVED_DEPS
    UNRESOLVED_DEPENDENCIES_VAR UNRESOLVED_DEPS
    PRE_INCLUDE_REGEXES vcruntime msvcp vcomp libomp libiomp
    PRE_EXCLUDE_REGEXES [Ss]ystem32/ api-ms- ext-ms- python libstd libgcc libc libm ld-linux
    POST_INCLUDE_REGEXES vcruntime msvcp vcomp libomp libiomp
    POST_EXCLUDE_REGEXES [Ss]ystem32/ api-ms- ext-ms- python libstd libgcc libc libm ld-linux
    DIRECTORIES 
)

foreach(_file ${RESOLVED_DEPS})
    file(INSTALL DESTINATION C:/Users/Quarter/PycharmProjects/sampo/sampo/native/cmake-build-release/modules/native/wheel/native TYPE SHARED_LIBRARY FOLLOW_SYMLINK_CHAIN FILES "${_file}")
endforeach()

endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Runtime" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND C:/Users/Quarter/AppData/Local/Programs/Python/Python310/python.exe setup.py WORKING_DIRECTORY C:/Users/Quarter/PycharmProjects/sampo/sampo/native/cmake-build-release/modules/native/wheel)
endif()

