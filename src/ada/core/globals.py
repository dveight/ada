"""Cross application globals are stored in this module for access in all DCC's without any application
specific references."""

from .ada_pb2 import Context

ALL_FILE_EXT = {Context.NUKE: ".nk", Context.MAYA: ".ma", Context.KATANA: ".kat", Context.GAFFER: ".gfr"}
