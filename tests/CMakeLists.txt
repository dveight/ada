# add custom target that has verbosity enabled
add_custom_target(check COMMAND ${CMAKE_CTEST_COMMAND} --verbose)

add_test(test_python_ada python2.7 -m nose -w ${CMAKE_CURRENT_SOURCE_DIR}/ada -vv -s)
if (NUKE_EXECUTABLE)
    add_test(test_nuke_python_ada ${NUKE_EXECUTABLE} --nukex -q -i -t ${PROJECT_SOURCE_DIR}/scripts/nuke_nosetests.py ${PROJECT_SOURCE_DIR}/tests/nuke)
endif()
