"""All packages below this one will be walked and auto imported this
way the developers do not have to bother with imports and any
additional packages will be automatically discovered.
"""
import pkgutil

from store import (
    REGISTERED_GLOBAL_BEFORE_CALLBACKS,
    REGISTERED_GLOBAL_AFTER_CALLBACKS,
    REGISTERED_TEMPLATE_AFTER_CALLBACKS,
    REGISTERED_TEMPLATE_BEFORE_CALLBACKS,
)

__path__ = pkgutil.extend_path(__path__, __name__)
for importer, modname, ispkg in pkgutil.walk_packages(
    path=__path__, prefix=__name__ + "."
):
    __import__(modname)

__all__ = [
    "REGISTERED_GLOBAL_BEFORE_CALLBACKS",
    "REGISTERED_GLOBAL_AFTER_CALLBACKS",
    "REGISTERED_TEMPLATE_AFTER_CALLBACKS",
    "REGISTERED_TEMPLATE_BEFORE_CALLBACKS",
]
