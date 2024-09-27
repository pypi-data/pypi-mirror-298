import copy
import sys
from collections import OrderedDict

from yaml import full_load


class InputBinding:
    def __init__(self, ib):
        self.position = ib.get("position", None)
        self.prefix = ib.get("prefix", None)


class OutputBinding:
    def __init__(self, ob):
        self.glob = ob.get("glob", None)


class Param:
    optional = False
    default = None
    type = None
    items = None

    def get_type(self):
        return self.type


class InputParam(Param):
    def __init__(self, param):
        if "id" not in param:
            raise Exception("Input without id")
        else:
            self.id = param["id"]

        self.type = param.get("type", None)
        self.items = []
        if type(self.type) is str and self.type[-2:] == "[]":
            self.items = []
            self.items.append(self.type[:-2])
            self.type = "array"
        if type(self.type) is list and self.type[0] == "null":
            self.optional = True
        elif type(self.type) is str and self.type[-1] == "?":
            self.optional = True
            self.type = self.type[:-1]
        else:
            self.optional = False

        if type(self.type) is dict:
            if "type" in self.type and "items" in self.type:
                if self.type["type"] == "array":
                    self.items = self.type["items"]
                    self.type = "array"

        self.description = param.get("doc", param.get("description", None))
        self.default = param.get("default", None)
        input_binding = param.get("inputBinding", None)
        if input_binding:
            self.input_binding = InputBinding(input_binding)
        self.stac_catalog = param.get("stac:catalog", None)

        if type(self.items) == str:
            s = self.items
            self.items = []
            self.items.append(s)


class Workflow:
    outputs = None
    inputs = None
    raw_workflow = None

    def __init__(self, cwl, startworkflowid=None):

        # retrieve starting workflow id if specified
        # store to to startworkflowid variable and remove it from file path
        try:
            file_cwl = cwl
            if hasattr(cwl, "rsplit") and startworkflowid is None and "#" in cwl:
                startworkflowid = cwl.rsplit("#", 1)[1]
                if startworkflowid == "":
                    raise ValueError("No value after the hashtag was found.")
                file_cwl = cwl.replace(f"#{startworkflowid}", "")

            with open(file_cwl) as f:
                self.raw_workflow = full_load(f)
        except AttributeError:
            self.raw_workflow = cwl
        except TypeError:
            self.raw_workflow = cwl

        if startworkflowid is not None:
            jworkflow = self.get_workflow_from_id(self.raw_workflow, startworkflowid)
        elif "$graph" in self.raw_workflow:
            jworkflow = self.graph_parser(self.raw_workflow)
        else:
            jworkflow = self.raw_workflow

        if jworkflow is None:
            raise ValueError("Wrong Workflow")

        try:
            self.tool_class = jworkflow["class"]
        except KeyError:
            sys.exit("`class` attribute of the CWL document not found")
        if self.tool_class != "Workflow":
            raise ValueError("Wrong Workflow class")

        self.inputs = OrderedDict()

        if type(jworkflow["inputs"]) is list:  # ids not mapped
            for param_dict in jworkflow["inputs"]:
                param = InputParam(param_dict)
                self.inputs[param.id] = param
        elif type(jworkflow["inputs"]) is dict:  # ids mapped
            for id, param_dict in jworkflow["inputs"].items():
                param_dict["id"] = id
                param = InputParam(param_dict)
                self.inputs[id] = param

        self.outputs = OrderedDict()
        if jworkflow["outputs"]:
            if type(jworkflow["outputs"]) is list:  # ids not mapped
                for param_dict in jworkflow["outputs"]:
                    param = InputParam(param_dict)
                    self.outputs[param.id] = param
            elif type(jworkflow["outputs"]) is dict:  # ids mapped
                for id, param_dict in jworkflow["outputs"].items():
                    param_dict["id"] = id
                    param = InputParam(param_dict)
                    self.outputs[id] = param
        self.description = jworkflow.get("doc", jworkflow.get("description", None))
        self.cwl_version = jworkflow.get("cwlVersion", "")
        self.id = jworkflow.get("id", "")

        # raw
        if "inputs" in jworkflow:
            self.raw_all_inputs = jworkflow["inputs"]
        else:
            self.raw_all_inputs = {}
        if "outputs" in jworkflow:
            self.raw_all_outputs = jworkflow["outputs"]
        else:
            self.raw_all_outputs = {}

    def get_inputs(self):
        return self.inputs

    def get_outputs(self):
        return self.outputs

    def get_raw_workflow(self):
        return self.raw_workflow

    @staticmethod
    def graph_parser(cwl):
        graph = cwl["$graph"]
        for it in graph:
            if "class" in it:
                if it["class"] == "Workflow":
                    return it

        return None

    @staticmethod
    def get_workflow_from_id(cwl, workflowid):
        graph = cwl["$graph"]
        for it in graph:
            if "class" in it:
                if it["class"] == "Workflow" and it["id"] == workflowid:
                    return it
        return None


class CWLParserTool:
    raw_workflow = None

    def __init__(self, cwl):
        try:
            with open(cwl.rsplit("#", 1)[0]) as f:
                self.raw_workflow = full_load(f)
        except AttributeError:
            self.raw_workflow = cwl

    def get_non_graph(self):
        out = []
        if self.raw_workflow is not None:
            for it in self.raw_workflow:
                if type(it) is str:
                    if it != "$graph":
                        out.append({it: self.raw_workflow[it]})
                    # if self.raw_workflow[it] != '$graph':
                    # out = copy.deepcopy(self.raw_workflow[it])

        return out

    def get_graph_classes(self):

        out = []

        if self.is_graph():
            graph = self.raw_workflow["$graph"]

            for it in graph:
                if type(graph) is dict:
                    pi = copy.deepcopy(graph[it])
                    pi["id"] = it
                    out.append(pi)
                elif type(graph) is list:
                    out.append(copy.deepcopy(it))

            # return copy.deepcopy(self.raw_workflow)

        return out

    def is_graph(self):
        if self.raw_workflow is not None:
            if type(self.raw_workflow) is dict:
                if "$graph" in self.raw_workflow:
                    return True

        return False
