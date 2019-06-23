cmake_minimum_required(VERSION 3.13)

set(ADA_PYTHON lib/python/ada)
set(ADA_CORE_INSTALL_PATH ${CMAKE_INSTALL_PREFIX}/${ADA_PYTHON})

set(ADA_PROTO_SOURCE ${PROJECT_SOURCE_DIR}/ada/proto)
set(ADA_COMPILE_OUT ${PROJECT_SOURCE_DIR}/ada/core)

set(ADA_NUKE_INSTALL_PATH ${CMAKE_INSTALL_PREFIX}/${ADA_PYTHON}/nuke)

add_custom_target(CREATE_ADA ALL DEPENDS proto/ada.proto proto/graph.proto)
add_custom_command(
        TARGET CREATE_ADA
        COMMAND protoc -I=${ADA_PROTO_SOURCE} --python_out=${ADA_COMPILE_OUT} ${ADA_PROTO_SOURCE}/ada.proto ${ADA_PROTO_SOURCE}/graph.proto
        COMMENT "Creating Ada python files."
        VERBATIM
)


file(INSTALL "__init__.py" DESTINATION ${ADA_CORE_INSTALL_PATH})

file(GLOB CORE_SRC "core/*.py" )

INSTALL(
    FILES ${CORE_SRC}
    DESTINATION ${ADA_CORE_INSTALL_PATH}/core
)

INSTALL(
    DIRECTORY core/nuke/
    DESTINATION ${ADA_CORE_INSTALL_PATH}/core/nuke
    FILES_MATCHING PATTERN "*.py")

INSTALL(
    DIRECTORY nuke/python/
    DESTINATION ${ADA_NUKE_INSTALL_PATH}
    FILES_MATCHING PATTERN "*.py"
)


