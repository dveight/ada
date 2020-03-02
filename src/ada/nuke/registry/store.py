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
        cls (Object): The class that is being used as a callback.
        kind (str): one of the callback_kinds from this module.

    Returns:
        object: A class object that contains the code to run for this
            callback.
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
    Decorator class for registering callbacks that run for
        every Ada template. This can be used to extend the 
        functionality of the system without adding code directly 
        to the base nuke project.

    Args:
        cls (Object): The class that is being used as a callback.
    
    Returns:
        object: A registered class. 
    """

    return register_callback(cls, "GLOBAL_BEFORE")


def register_template_callback_before(cls):
    """
    Decorator class for registering template specific callbacks
        that run before executing the Ada graph.

    Args:
        cls (Object): The class that is being used as a callback.
    
    Returns:
        object: A registered class. 
    """

    return register_callback(cls, "TEMPLATE_BEFORE")


def register_template_callback_after(cls):
    """
    Decorator class for registering template specific callbacks
        that run after executing the Ada graph.

    Args:
        cls (Object): The class that is being used as a callback.
    
    Returns:
        object: A registered class. 
    """
    return register_callback(cls, "TEMPLATE_AFTER")


def register_global_callback_after(cls):
    """
    Decorator class for registering global callbacks
        that run for every template executed. Adding callbacks
        should be the norm for extending the core functionality
        of the system.

    Args:
        cls (Object): The class that is being used as a callback.
    
    Returns:
        object: A registered class. 
    """

    return register_callback(cls, "GLOBAL_AFTER")
