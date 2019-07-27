# helper vartiables for install paths
set(ADA_CORE_INSTALL_PATH ${CMAKE_INSTALL_PREFIX}/lib/python)
set(ADA_PROTO_SOURCE ${CMAKE_CURRENT_SOURCE_DIR}/proto)
set(ADA_COMPILE_OUT ${CMAKE_CURRENT_SOURCE_DIR}/ada/core)

# compile the protobuffers into our src structure
add_custom_target(CREATE_ADA ALL DEPENDS proto/ada.proto proto/graph.proto)
add_custom_command(
        TARGET CREATE_ADA
        COMMAND protoc -I=${ADA_PROTO_SOURCE} --python_out=${ADA_COMPILE_OUT} ${ADA_PROTO_SOURCE}/ada.proto ${ADA_PROTO_SOURCE}/graph.proto
        COMMENT "Creating Ada python files."
        VERBATIM
)

function (generate_executable_py APPLICATION)
    # creates the dynamically generated executable.py file which hard codes the nuke application at cmake build time
    string(TOLOWER ${APPLICATION} APPLICATION_LOWER)
    set(EXECUTABLE_PY "import os\n\n${APPLICATION}_EXECUTABLE = os.getenv(\"ADA_${APPLICATION}_EXECUTABLE\", \"${${APPLICATION}_EXECUTABLE}\")\n")
    file(WRITE ${CMAKE_CURRENT_SOURCE_DIR}/ada/core/${APPLICATION_LOWER}/executable.py ${EXECUTABLE_PY})
endfunction()

# add the nuke and gaffer executables
generate_executable_py(NUKE)
generate_executable_py(GAFFER)

# copy over all of the python and tickle files found under the current source directory
# explicily add the on the fly compiled protobufs
file(GLOB_RECURSE SOURCE_LIST RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "*.py")
list(APPEND SOURCE_LIST "ada/core/ada_pb2.py" "ada/core/graph_pb2.py")
foreach(FILE_PATH ${SOURCE_LIST})
    get_filename_component(DIR_PATH ${FILE_PATH} DIRECTORY)
    install(FILES ${FILE_PATH} DESTINATION ${ADA_CORE_INSTALL_PATH}/${DIR_PATH})
endforeach()
