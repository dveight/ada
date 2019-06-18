from ....store import register_global_callback_before
import nuke


@register_global_callback_before
class CleanUpAdaTabs:
    name = "Root frame range example"

    def __init__(self):
        self.node = nuke.Root()

    @classmethod
    def run(cls):
        nuke.Root()["first_frame"].setValue(1000)
        nuke.Root()["last_frame"].setValue(2000)
