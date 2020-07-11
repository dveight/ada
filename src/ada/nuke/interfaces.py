"""
Tab Api 
    Ada Tab (uses tab api) -> Makes an Ada tab 
        Defaults:
            queue order: [1], bake mode [gui & terminal, terminal only, gui only, do not bake] - > should be plugins
            Actions: [choice] (Add Action) 
                -> Looks action using zope registry
                -> Calls the knobs function on the class returning a list of knobs.
                -> Adds knob with Ada:{action_name}:{label}:{idx}
                -> Adds a enabled [x] boolean to the left and a 'delete' button to the right [delete]
            Divider
"""

from zope import interface


class IAdaAction(interface.Interface):
    """
    Actions define the core of the new Ada tab
    api this is so we can extend the functionality
    of the tab within Nuke withough having to update
    the core template Engine. The engine will lookup
    the action registred through zope. 

    """

    # name of the action, this will be the name of
    # the action in the Enumeration Knob, the Ada
    # tab will automatically lookup all of the
    # registered actions adding in sorted order.
    display_name = interface.Attribute("Display Name")
    action_name = interface.Attribute("Action Name")
    applies_to = interface.Attribute(
        "Node classes that this action will apply to. Default is every node."
    )

    def process(knobs=None):
        """
        Core function that all actions must implement.

        Ada will go over all the knobs picking up knobs
        starting with __ada_action_{action}_{index}

        the {action} will be exracted and then executed:

        Action(current_action).execute()

        """

    def knobs(node=None):
        """
        Add the knobs for the action to the node. Each
        action should implement a unique set of knobs.

        When the user clicks the add button the action
        in the Enumeration Knob will be looked up and
        this function will be called.

        """

