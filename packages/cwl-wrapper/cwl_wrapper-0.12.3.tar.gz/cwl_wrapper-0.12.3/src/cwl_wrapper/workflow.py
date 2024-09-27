import sys

from loguru import logger

from .cwl.t2cwl import Workflow as CWLWorkflow
from .rulez import Rulez

logger.add(sys.stderr, level="INFO")


class Directory:
    is_array = False
    is_optional = False
    id: str = None

    def __init__(self, id: str, is_array, is_optional=False, raw=None):
        self.id = id
        self.is_array = is_array
        self.is_optional = is_optional
        self.raw = raw

    def __str__(self):
        return str({"id": self.id, "is_array": self.is_array, "is_optional": self.is_optional})


def parse_cwl_param_directory(vals: dict):
    res = []
    for it in vals:
        cwl_param = vals[it]  # cwl_param is of type InputParam
        # logger.debug(f"{type(cwl_param)} {it} - {cwl_param.type}")

        if cwl_param.type in ["Directory"]:
            res.append(
                Directory(
                    id=cwl_param.id,
                    is_array=False,
                    is_optional=cwl_param.optional,
                    raw=cwl_param,
                )
            )

        elif cwl_param.type == "array":
            for it in cwl_param.items:
                if type(it) == str and it in ["Directory"]:
                    res.append(
                        Directory(
                            id=cwl_param.id,
                            is_array=True,
                            is_optional=cwl_param.optional,
                            raw=cwl_param,
                        )
                    )
                    break

    return res


class Workflow:
    wf = None
    driver = None

    def __init__(self, cwl, rulez: Rulez, startworkflowid: str = None):
        # print(args)
        if rulez.get("/parser/driver") == "cwl":
            self.wf = CWLWorkflow(cwl, startworkflowid)
            self.driver = "cwl"
        else:
            raise ValueError("Rules driver not found or unknown")

    def get_raw_all_inputs(self):
        return self.wf.raw_all_inputs

    def get_raw_all_outputs(self):
        return self.wf.raw_all_outputs

    def get_raw_inputs(self):
        return self.wf.get_inputs()

    def get_raw_outputs(self):
        return self.wf.get_outputs()

    def get_inputs_directory(self):
        if self.driver == "cwl":
            return parse_cwl_param_directory(self.get_raw_inputs())

    def get_outputs_directory(self):
        if self.driver == "cwl":
            return parse_cwl_param_directory(self.get_raw_outputs())

    def get_raw_workflow(self):
        return self.wf.get_raw_workflow()

    def get_id(self):
        if self.driver == "cwl":
            return self.wf.id

        return ""

    def __str__(self):
        return "workflow"  # "#self.wf['id']


class CWL:
    pass
