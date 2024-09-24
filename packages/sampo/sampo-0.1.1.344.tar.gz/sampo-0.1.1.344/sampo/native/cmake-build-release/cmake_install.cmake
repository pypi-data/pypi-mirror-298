# Install script for directory: C:/Users/Quarter/PycharmProjects/sampo/sampo/native

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

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("C:/Users/Quarter/PycharmProjects/sampo/sampo/native/cmake-build-release/third_party/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("C:/Users/Quarter/PycharmProjects/sampo/sampo/native/cmake-build-release/modules/cmake_install.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "no_use" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE MODULE FILES "C:/Users/Quarter/PycharmProjects/sampo/sampo/native/cmake-build-release/native.pyd")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "no_use" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE FILES "C:/Users/Quarter/PycharmProjects/sampo/sampo/native/cmake-build-release/TARGETS.exe")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "IN_LIST" OR NOT CMAKE_INSTALL_COMPONENT)
  file(GET_RUNTIME_DEPENDENCIES
    RESOLVED_DEPENDENCIES_VAR _CMAKE_DEPS
    EXECUTABLES
      "C:/Users/Quarter/PycharmProjects/sampo/sampo/native/cmake-build-release/TARGETS.exe"
    MODULES
      "C:/Users/Quarter/PycharmProjects/sampo/sampo/native/cmake-build-release/native.pyd"
    PRE_INCLUDE_REGEXES
      "vcruntime"
      "msvcp"
      "vcomp"
      "libomp"
      "libiomp"
    PRE_EXCLUDE_REGEXES
      "[Ss]ystem32/"
      "api-ms-"
      "ext-ms-"
      "python"
      "libstd"
      "libgcc"
      "libc"
      "libm"
      "ld-linux"
    POST_INCLUDE_REGEXES
      "vcruntime"
      "msvcp"
      "vcomp"
      "libomp"
      "libiomp"
    POST_EXCLUDE_REGEXES
      "[Ss]ystem32/"
      "api-ms-"
      "ext-ms-"
      "python"
      "libstd"
      "libgcc"
      "libc"
      "libm"
      "ld-linux"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "IN_LIST" OR NOT CMAKE_INSTALL_COMPONENT)
  foreach(_CMAKE_TMP_dep IN LISTS _CMAKE_DEPS)
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES ${_CMAKE_TMP_dep}
      FOLLOW_SYMLINK_CHAIN)
  endforeach()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Runtime" OR NOT CMAKE_INSTALL_COMPONENT)
  file(GET_RUNTIME_DEPENDENCIES
    RESOLVED_DEPENDENCIES_VAR _CMAKE_DEPS
    EXECUTABLES
      "C:/Users/Quarter/PycharmProjects/sampo/sampo/native/cmake-build-release/TARGETS.exe"
    MODULES
      "C:/Users/Quarter/PycharmProjects/sampo/sampo/native/cmake-build-release/native.pyd"
    PRE_INCLUDE_REGEXES
      "vcruntime"
      "msvcp"
      "vcomp"
      "libomp"
      "libiomp"
    PRE_EXCLUDE_REGEXES
      "[Ss]ystem32/"
      "api-ms-"
      "ext-ms-"
      "python"
      "libstd"
      "libgcc"
      "libc"
      "libm"
      "ld-linux"
    POST_INCLUDE_REGEXES
      "vcruntime"
      "msvcp"
      "vcomp"
      "libomp"
      "libiomp"
    POST_EXCLUDE_REGEXES
      "[Ss]ystem32/"
      "api-ms-"
      "ext-ms-"
      "python"
      "libstd"
      "libgcc"
      "libc"
      "libm"
      "ld-linux"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Runtime" OR NOT CMAKE_INSTALL_COMPONENT)
  foreach(_CMAKE_TMP_dep IN LISTS _CMAKE_DEPS)
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES ${_CMAKE_TMP_dep}
      FOLLOW_SYMLINK_CHAIN)
  endforeach()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Development" OR NOT CMAKE_INSTALL_COMPONENT)
  file(GET_RUNTIME_DEPENDENCIES
    RESOLVED_DEPENDENCIES_VAR _CMAKE_DEPS
    EXECUTABLES
      "C:/Users/Quarter/PycharmProjects/sampo/sampo/native/cmake-build-release/TARGETS.exe"
    MODULES
      "C:/Users/Quarter/PycharmProjects/sampo/sampo/native/cmake-build-release/native.pyd"
    PRE_INCLUDE_REGEXES
      "vcruntime"
      "msvcp"
      "vcomp"
      "libomp"
      "libiomp"
    PRE_EXCLUDE_REGEXES
      "[Ss]ystem32/"
      "api-ms-"
      "ext-ms-"
      "python"
      "libstd"
      "libgcc"
      "libc"
      "libm"
      "ld-linux"
    POST_INCLUDE_REGEXES
      "vcruntime"
      "msvcp"
      "vcomp"
      "libomp"
      "libiomp"
    POST_EXCLUDE_REGEXES
      "[Ss]ystem32/"
      "api-ms-"
      "ext-ms-"
      "python"
      "libstd"
      "libgcc"
      "libc"
      "libm"
      "ld-linux"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Development" OR NOT CMAKE_INSTALL_COMPONENT)
  foreach(_CMAKE_TMP_dep IN LISTS _CMAKE_DEPS)
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES ${_CMAKE_TMP_dep}
      FOLLOW_SYMLINK_CHAIN)
  endforeach()
endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "C:/Users/Quarter/PycharmProjects/sampo/sampo/native/cmake-build-release/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
