
from zope.interface import implements
from ada.nuke.interfaces import IAdaAction 

@implements(IAdaAction)
class PrintAction(node):
    def __init__(self):
        self.action_name = "print"
        self.help = "Prints Hello to the user."
        self.display_name = "Print

    def process(self, knobs):

        nuke.tprint(
            "Hello from: {knob}".format(knobs.get("print"))
        )

    def knobs(self):
        """
        Should we be using knobby here? I like how it works
        but it needs some extra things to make it nice.

        """
 
        hello_knob = nuke.Text_Knob(
            "print",
            "Print This",
            "Test"
        )
        return [hello_knob]
