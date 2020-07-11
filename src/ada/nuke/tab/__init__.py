from rsp.nuke.ada.tab import AdaTab


class AdaTab(object):
    def __init__(self, node):
        NotImplemented

    def add_action(self):
        """
        Add an action to the node based on the selected
        action which is driven from the list of registered
        actions that can be created by td's or artists. 

        """
        NotImplemented

    def create(self):
        """
        Create an ada tab on the node
        """
        NotImplemented

    def actions(self):
        """
        For the current tab iterate over the actions the 
        user has added and return a list of objects which 
        represent each action.

        """
        NotImplemented

    def version(self):
        """
        Return the version of the tab on the current node.

        """
        NotImplemented

    def latest_version(self):
        """
        Return the latest version of the Ada tab.

        """
        NotImplemented
