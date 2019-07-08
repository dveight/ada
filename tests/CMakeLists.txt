# add custom target that has verbosity enabled
add_custom_target(check COMMAND ${CMAKE_CTEST_COMMAND} --verbose)

add_test(test_python_ada python2.7 -m nose -w ${CMAKE_CURRENT_SOURCE_DIR}/ada -vv -s)

if (NUKE_EXECUTABLE)
    add_test(test_nuke_python_ada ${NUKE_EXECUTABLE} --nukex -q -i -t ${CMAKE_CURRENT_SOURCE_DIR}/nosetests.py ${CMAKE_CURRENT_SOURCE_DIR}/nuke)
endif()

if (GAFFER_EXECUTABLE)
    add_test(test_gaffer_python_ada ${GAFFER_EXECUTABLE} python ${CMAKE_CURRENT_SOURCE_DIR}/nosetests.py ${CMAKE_CURRENT_SOURCE_DIR}/gaffer)
endif()
