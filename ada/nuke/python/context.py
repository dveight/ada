"""This module contains the code for executing the nodes in Nuke that have Ada tabs attached
to them. We find all nodes through all groups and accumulate them into queues waiting to be
processed by the server. Each queue is executed in alpha-numeric order. Support for check pointing
in GUI mode will be supported.
"""
import re
from itertools import groupby

import nuke
from registry.store import callback_kinds
from ada.core.common import getLog


class Engine:
    """
    Engine is the core class for executing Ada in Nuke. When passing a template in from the cli the static method
    fuel is called to inject the user specified template into nuke then all the nodes will be gathered and executed
    in the order determined by the user.

    """

    def __init__(self):
        self.input_nodes = []
        self.nodes_to_bake = []
        self.template_class = None

    @staticmethod
    def fuel(template):
        """
        Fuel an empty script with a template and set the basic things
            that are required. Views should be handled here but inherited
            from the template graph file.

        Args:
            template (str): Path to template nuke script.

        """
        getLog().info("Ada: Fuel begin.")

        nuke.scriptOpen(template)
        template = nuke.Ada.template.location

        try:
            getLog().info("Ada: Reading template: {0}".format(template))
            nuke.scriptReadFile(template)

        except RuntimeError as err:
            getLog().warning("Ada: '{0}'".format(err))

        start = nuke.Ada.script_frame_range.start
        end = nuke.Ada.script_frame_range.end

        root = nuke.Root()
        root["first_frame"].setValue(start)
        root["last_frame"].setValue(end)

        getLog().info("Ada: setting root range: start: {0}, end: {1}".format(start, end))

        getLog().info("Ada: Fuel end.")

    @classmethod
    def run(cls, nodes=None, bake_list=None, pause=None):
        """
        Once the nodes are gathered up then we can iterate over them
        and execute each knob on the tab from the top to the bottom.

        Args:
            nodes (list): Un-sorted nodes either a selection in Nuke.
            bake_list (list): List of nodes to be processed, these
                have already been gathered and sorted.
            pause (int): The queue order which you want to stop at.

        Returns:
            list: all the nodes which were executed successfully.
        """
        # any nuke script can add a __template_class_text knob to its
        # root node and register a callback against it
        cls.template_class = (
            nuke.Root()
            .knobs()
            .get("__template_class__", nuke.Text_Knob("null", "null"))
            .value()
        )
        cls.template_class = None if cls.template_class == "" else cls.template_class

        # if we are not continuing a previous bake, then we need to
        # gather, sort and validate the nodes.
        if not bake_list:
            cls.input_nodes = nodes or nuke.allNodes(recurseGroups=True)
            gathered_nodes = cls.gather(cls.input_nodes)
            bake_list = cls.alpha_numeric_sort(gathered_nodes)

            getLog().info("Ada: Nodes to bake: {0}".format(bake_list))

        # run validation code / frame work before executing tabs
        cls.validate(bake_list)

        # queue nodes for baking
        queue = cls.queue(bake_list)
        getLog().info("template class: {}".format(cls.template_class))

        # execute registered global/template callbacks before
        cls.execute_callbacks("GLOBAL_BEFORE")
        cls.execute_callbacks("TEMPLATE_BEFORE", template_class=cls.template_class)

        # process the nodes which have ada tabs
        results = cls.process(queue, bake_list, pause)

        # execute registered global/template callbacks after
        cls.execute_callbacks("TEMPLATE_AFTER")
        cls.execute_callbacks("GLOBAL_AFTER", template_class=cls.template_class)

        return results

    @staticmethod
    def gather(nodes):
        """
        Gather up all nuke nodes for Ada Tab.

        Returns:
            nodes (list): list of node names.
        """
        nodes_to_process = []
        for node in nodes:
            if node.knobs().get("ada"):
                do_not_bake = node["do_not_bake"].value()
                if do_not_bake:
                    continue
                nodes_to_process.append(node.fullName())

        def convert(text):
            return int(text) if text.isdigit() else text

        return sorted(
            nodes_to_process,
            key=lambda _nodes: [convert(node) for node in re.split("([0-9]+)", _nodes)],
        )

    @staticmethod
    def alpha_numeric_sort(nodes):
        """
        Sort all node names alpha numerically.

        Args:
            nodes (str): List of node full names.

        Returns:
            list (str): A list of sorted node names.
        """

        def convert(text):
            return int(text) if text.isdigit() else text

        return sorted(
            nodes,
            key=lambda _nodes: [convert(node) for node in re.split("([0-9]+)", _nodes)],
        )

    @staticmethod
    def validate(full_node_names):
        """
        Run validation checks that need to happen before executing.

        Args:
            full_node_names (str): Full node name of the current node
                we are validating.

        """
        for node_name in full_node_names:
            node = nuke.toNode(node_name)
            while node.knobs().get("__run"):
                node.removeKnob(node["__run"])

    @staticmethod
    def queue(full_node_names):
        """
        Queue nodes in the same execution order to be processed together alpha numerically.

        Args:
            full_node_names (list): Sorted node names in alphanumeric order.

        Returns:
            itertools.groupby: Groups of node names to execute together.
        """

        def order(node_name):
            try:
                return int(nuke.toNode(node_name).knob("queue_order").value())
            except KeyError:
                return 0

        all_nodes = sorted(full_node_names, key=order)
        queues = groupby(all_nodes, key=order)
        return queues

    @classmethod
    def execute_callbacks(cls, kind, template_class=None):
        """
        Callbacks are registered as global before/after or template specific.

        Args:
            kind (str): The callback group we want to execute.
            template_class (str): Script class name stored on the root node of Nuke.

        """
        cbs_to_execute = callback_kinds[kind]
        cb_message = "Ada: Executing {kind} callback: {name}"
        for callback_name in cbs_to_execute:
            if kind.startswith("GLOBAL"):
                getLog().info(
                    cb_message.format(
                        kind=" ".join(kind.lower().split("_")),
                        name=callback_name
                    )
                )
                for cb in cbs_to_execute[callback_name]:
                    cb.run()

            if kind.startswith("TEMPLATE") and template_class == callback_name:
                getLog().info(
                    cb_message.format(
                        kind=" ".join(kind.lower().split("_")),
                        name=callback_name
                    )
                )
                for cb in cbs_to_execute[callback_name]:
                    cb.run()

    @classmethod
    def process(cls, queues, all_nodes, break_point):
        """
        Bulk of the work happens here, knobs are baked, set, buttons are pressed, code is executed etc.

        Args:
            queues (itertools.groupby): Groups of nodes to process.
            all_nodes (list): List of all nodes to bake.
            break_point (int): Point at which we want Ada to stop executing to inspect something.

        Returns:
            list: Nodes which were successfully execute.
        """
        processed_nodes = []
        for queue_order, queue in queues:
            getLog().info("Ada: Executing Queue: {0}".format(queue_order))

            if queue_order == break_point:
                to_process = list(set(all_nodes) - set(processed_nodes))
                return to_process

            for node_name in list(queue):
                node = nuke.toNode(node_name)
                getLog().info("  Ada: Executing Node {0}".format(node.name()))
                # this is where values are converted from ada
                # expressions to serialised values.
                cls.bake_knobs(node)
                cls.set_knobs(node)

                # buttons are pressed if added in the Ada tab.
                cls.execute_buttons(node)

                # finally code is executed.
                cls.execute_code(node)

                # if all goes well return the node we just processed
                # to the list of processed nodes.
                processed_nodes.append(node_name)

        return processed_nodes

    @classmethod
    def bake_knobs(cls, node):
        """
        Take the string in the knobs to bake knob and then create a list of knobs to run bake_knob on.

        Args:
            node (nuke.Node): current node we are baking in the queue.
        """
        if node.knob("knobs_to_bake") and node.knob("knobs_to_bake").value():
            # get bake knob list, split, and strip white space
            knobs = node.knob("knobs_to_bake").value()
            raw_knobs_to_set = knobs.split(",")

            for raw_knob in raw_knobs_to_set:
                knob = raw_knob.strip()

                getLog().info("   Ada: Baking Knob: {0}.{1}".format(node.name(), knob))
                cls.bake_knob(node, knob)

    @classmethod
    def set_knobs(cls, node):
        """
        Set values from context on a given knob.

        Args:
            node (nuke.Node): current node we are baking in the queue.
        """

        if node.knob("set_knobs") and node.knob("set_knobs").value():
            # get set knob list, split, and strip white space
            knobs = node.knob("knobs_to_set").value()
            raw_knobs_to_set = knobs.split(",")

            for raw_knob in raw_knobs_to_set:
                try:
                    knob = raw_knob.strip()
                    # clean up any spaces
                    raw_name, raw_value = knob.split("=")
                    name = raw_name.strip()
                    value = raw_value.strip()

                    getLog().info("Ada: Knobs to set: {0} : {1}".format(name, value))
                    cls.bake_knob(node, name, value=value)
                except ValueError:
                    msg = "Unable to set: {0} missing value after '='"
                    getLog().warning(msg.format(node.name()))

    @staticmethod
    def bake_knob(node, name, value=None):
        """
        Function to set a knob using knob=value or bake the knob directly.

        Args:
            node (nuke.Node): A node we are trying to bake a knob on.
            name (str): The knob name we are trying to set.
            value ([Optional str]): If value is None execute the
        """
        knob = node.knob(name)
        if not knob:
            return

        if value is None:
            if isinstance(knob, nuke.Array_Knob):
                views = nuke.views()
                start = nuke.Ada.script_frame_range.start
                end = nuke.Ada.script_frame_range.end
                for view in views:
                    curves = knob.animations(view)
                    for curve in curves:
                        values = set()
                        index = curve.knobIndex()
                        for frame in range(start, end + 1):
                            knob.setKeyAt(frame, index, view)
                            value = curve.evaluate(frame)
                            values.add(value)
                            knob.setValueAt(value, frame, index, view)

                        if len(values) > 1:
                            knob.setExpression("curve", channel=index, view=view)
                        else:
                            knob.clearAnimated()  # "BAKE"

            elif isinstance(knob, nuke.File_Knob):
                knob.setValue(str(nuke.tcl("subst", knob.value())))

            elif isinstance(knob, nuke.EvalString_Knob):
                knob.setValue(knob.evaluate())
            else:
                getLog().warning(
                    "{}.{} unsupported knob type {}".format(
                        node.name(), name, type(knob)
                    )
                )
        else:
            try:
                knob.clearAnimated()
            except AttributeError:
                pass
            try:
                if isinstance(knob, nuke.Int_Knob):
                    knob.setValue(int(value))
                elif isinstance(knob, nuke.Enumeration_Knob):
                    try:
                        knob.setValue(int(value))
                    except ValueError:
                        knob.setValue(str(value))
                elif isinstance(knob, nuke.Array_Knob):
                    knob.setValue(float(value))
                else:
                    knob.setValue(value)
            except TypeError as ee:
                getLog().warning(
                    "Ada: set {}.{}={} TypeError: {}".format(
                        node.name(), name, value, ee
                    )
                )
            except ValueError as ee:
                getLog().warning(
                    "Ada: set {}.{}={} ValueError: {}".format(
                        node.name(), name, value, ee
                    )
                )

    @staticmethod
    def execute_code(node):
        """
        Take code from multi-eval stringe knob, put it in a button
        then execute the button. This allows the user to to create
        complex python script on nodes and reference nuke.thisNode().

        Args:
            node (nuke.Node): Node that hasa execute_code knob.

        Returns:
            bool: True if code execution is fine, otherwise false.
        """

        if node.knob("execute_code") and node.knob("execute_code").value():
            success = False
            # execute code inside a temp knob attached to the node
            py_script_knob = nuke.PyScript_Knob("__run", "Run")
            node.addKnob(py_script_knob)
            code = node.knob("code_to_execute").toScript()
            try:
                py_script_knob.setValue(code)
                py_script_knob.execute()
                success = True
            except Exception as e:
                getLog().warning(
                    "'{0}' failed to execute code:\n{1}\nreason:\n\t{2}\n".format(
                        node.fullName(), code, e
                    )
                )
            finally:
                node.removeKnob(py_script_knob)
                return success

    @staticmethod
    def execute_buttons(node):
        """
        Execute any buttons the user has added to the execute knobs list.

        Args:
            node (nuke.Node): The node we are currently baking.
        """
        if node.knob("execute_knobs") and node.knob("execute_knobs").value():
            # get button list, split, and strip white space
            buttons = node.knob("knobs_to_execute").value()
            raw_knobs_to_exec = buttons.split(",")

            for raw_knob in raw_knobs_to_exec:
                knob = raw_knob.strip()
                knob_object = node.knob(knob)
                if not knob_object or not hasattr(knob_object, "execute"):
                    getLog().warning(
                        "Executing knob: '{0}' not found on node '{1}'".format(
                            knob, node.name()
                        )
                    )
                else:
                    getLog().info("Ada: Button to execute: {0}".format(knob))
                    knob_object.setFlag(0x0000000000010000)
                    knob_object.execute()
