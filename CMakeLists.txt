cmake_minimum_required(VERSION 3.13)

add_subdirectory(apps)
add_subdirectory(src)
add_subdirectory(scripts)
add_subdirectory(extern)

enable_testing()
add_subdirectory(tests)
