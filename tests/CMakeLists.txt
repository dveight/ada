# add custom target that has verbosity enabled
add_custom_target(check COMMAND ${CMAKE_CTEST_COMMAND} --verbose)

add_test(test_python_ada python2.7 -m nose -w ${CMAKE_CURRENT_SOURCE_DIR}/ada -vv -s)

function(add_ada_test APPLICATION)
    # adds a per application tests if either the cmake or environment variables are set
    # cmake looks for ${APPLICATION}_EXECUTABLE
    # environment looks for ADA_${APPLICATION}_EXECUTABLE
    set(APPLICATION_VARIABLES ${ARGN})
    if (DEFINED ENV{ADA_${APPLICATION}_EXECUTABLE})
        set(${APPLICATION}_EXECUTABLE $ENV{ADA_${APPLICATION}_EXECUTABLE})
    endif()
    if (${APPLICATION}_EXECUTABLE)
        string(TOLOWER ${APPLICATION} APPLICATION_LOWER)
        add_test(
            NAME test_${APPLICATION_LOWER}_python_ada
            COMMAND ${${APPLICATION}_EXECUTABLE} ${APPLICATION_VARIABLES} ${CMAKE_CURRENT_SOURCE_DIR}/nosetests.py ${CMAKE_CURRENT_SOURCE_DIR}/${APPLICATION_LOWER}
        )
    endif()
endfunction()

add_ada_test(NUKE -t -q -i --nukex)
add_ada_test(GAFFER python)
