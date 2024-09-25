file(
    GET_RUNTIME_DEPENDENCIES
    LIBRARIES $<TARGET_FILE:native>
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
