from ....store import register_template_callback_before
import nuke


@register_template_callback_before
class SetFrameRange:
    name = "TestTemplate"

    def __init__(self):
        self.node = None

    @classmethod
    def run(cls):
        print "Running some callback code!"
