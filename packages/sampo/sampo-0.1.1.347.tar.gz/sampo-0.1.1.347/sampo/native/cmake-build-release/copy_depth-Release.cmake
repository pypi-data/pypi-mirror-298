file(
    GET_RUNTIME_DEPENDENCIES
    LIBRARIES C:/Users/Quarter/PycharmProjects/sampo/sampo/native/cmake-build-release/native.pyd C:/Users/Quarter/PycharmProjects/sampo/sampo/native/cmake-build-release/TARGETS.exe
    RESOLVED_DEPENDENCIES_VAR RESOLVED_DEPS
    UNRESOLVED_DEPENDENCIES_VAR UNRESOLVED_DEPS
    PRE_INCLUDE_REGEXES vcruntime msvcp vcomp libomp libiomp
    PRE_EXCLUDE_REGEXES [Ss]ystem32/ api-ms- ext-ms- python libstd libgcc libc libm ld-linux native TARGETS
    POST_INCLUDE_REGEXES vcruntime msvcp vcomp libomp libiomp
    POST_EXCLUDE_REGEXES [Ss]ystem32/ api-ms- ext-ms- python libstd libgcc libc libm ld-linux native TARGETS
    DIRECTORIES 
)

file(COPY ${RESOLVED_DEPS} DESTINATION C:/Users/Quarter/PycharmProjects/sampo/sampo/native/cmake-build-release FOLLOW_SYMLINK_CHAIN)
