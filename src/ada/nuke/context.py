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
from ada.nuke.tab import AdaTab


class Engine(object):
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

        getLog().info(
            "Ada: setting root range: start: {0}, end: {1}".format(start, end)
        )

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
                        kind=" ".join(kind.lower().split("_")), name=callback_name
                    )
                )
                for cb in cbs_to_execute[callback_name]:
                    cb.run()

            if kind.startswith("TEMPLATE") and template_class == callback_name:
                getLog().info(
                    cb_message.format(
                        kind=" ".join(kind.lower().split("_")), name=callback_name
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

                # get tab or whatever this will be is an api that extracts a
                # tab from a node, this is an adapater of a interface class
                AdaTab(node).process()
                processed_nodes.append(node)

        return processed_nodes

