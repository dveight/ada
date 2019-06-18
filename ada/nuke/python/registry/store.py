"""This is where we store the created dicts of callbacks for
global and template execution"""

REGISTERED_GLOBAL_BEFORE_CALLBACKS = {}
REGISTERED_GLOBAL_AFTER_CALLBACKS = {}

REGISTERED_TEMPLATE_AFTER_CALLBACKS = {}
REGISTERED_TEMPLATE_BEFORE_CALLBACKS = {}

callback_kinds = {
    "GLOBAL_BEFORE": REGISTERED_GLOBAL_BEFORE_CALLBACKS,
    "GLOBAL_AFTER": REGISTERED_GLOBAL_AFTER_CALLBACKS,
    "TEMPLATE_BEFORE": REGISTERED_TEMPLATE_BEFORE_CALLBACKS,
    "TEMPLATE_AFTER": REGISTERED_TEMPLATE_AFTER_CALLBACKS,
}


def register_callback(cls, kind):
    """
    Args:
        cls:
        kind:

    Returns:

    """
    registered_callbacks = callback_kinds.get(kind)

    if cls.name in registered_callbacks:
        callbacks = registered_callbacks[cls.name]
        callbacks.append(cls)
        registered_callbacks[cls.name] = callbacks
    else:
        registered_callbacks[cls.name] = [cls]

    return cls


def register_global_callback_before(cls):
    """
    Decorator class for registering after run pre template callbacks
    Args:
        cls:
    Returns:

    """

    return register_callback(cls, "GLOBAL_BEFORE")


def register_template_callback_before(cls):
    """
    Decorator class for registering before run pre template callbacks
    Args:
        cls:

    Returns:

    """

    return register_callback(cls, "TEMPLATE_BEFORE")


def register_template_callback_after(cls):
    """
    Decorator class for registering after run pre template callbacks
    Args:
        cls:
    Returns:

    """
    return register_callback(cls, "TEMPLATE_AFTER")


def register_global_callback_after(cls):
    """
    Decorator class for registering after run pre template callbacks
    Args:
        cls:
    Returns:

    """

    return register_callback(cls, "GLOBAL_AFTER")
