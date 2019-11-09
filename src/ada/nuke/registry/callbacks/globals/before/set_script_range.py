from ....store import register_global_callback_before
import nuke


@register_global_callback_before
class SetScriptRange:
    name = "Root frame range example"

    def __init__(self):
        self.node = nuke.Root()

    @classmethod
    def run(cls):
        """Put code here to run before a template executes"""
        print "executing callback!"

