# add custom target that has verbosity enabled
add_custom_target(check COMMAND ${CMAKE_CTEST_COMMAND} --verbose)
add_test(test_python_ada nosetests -w ${CMAKE_CURRENT_SOURCE_DIR} -vv -s)