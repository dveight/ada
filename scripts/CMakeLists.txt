set(ADA_SCRIPTS_INSTALL_PATH ${CMAKE_INSTALL_PREFIX}/bin)

INSTALL(FILES ada
    DESTINATION ${ADA_SCRIPTS_INSTALL_PATH}
    PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ
    GROUP_EXECUTE GROUP_READ
)
INSTALL(
    FILES graph_parser
    DESTINATION ${ADA_SCRIPTS_INSTALL_PATH}
    PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ
    GROUP_EXECUTE GROUP_READ
)
