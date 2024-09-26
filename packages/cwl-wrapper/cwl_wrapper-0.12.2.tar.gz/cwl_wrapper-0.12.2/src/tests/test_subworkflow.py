import filecmp
import os
import tempfile
import unittest

import yaml
from click.testing import CliRunner
from cwl_wrapper import app
from cwl_wrapper.parser import Parser


class TestSubworkflowCwl(unittest.TestCase):
    def setUp(self):
        self.stagein_cwl_file = os.path.join(os.path.dirname(__file__), "data/stagein.cwl")
        self.stageout_cwl_file = os.path.join(os.path.dirname(__file__), "data/stageout.cwl")
        self.app_cwl_file = os.path.join(os.path.dirname(__file__), "data/dNBR.cwl")
        self.expected_wrapped_cwl = os.path.join(
            os.path.dirname(__file__), "data/test_dNBR_expected.cwl"
        )
        self.expected_usage_test = os.path.join(os.path.dirname(__file__), "data/test_help_expected.txt")
        self.temp_output_file = tempfile.NamedTemporaryFile()

    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(app.main, ["--help"])
        with open(self.expected_usage_test) as f:
            contents = f.read()
            assert result.output.strip() == contents.strip()

    def test_dNBR(self):
        runner = CliRunner()
        result = runner.invoke(
            app.main,
            [
                "--stagein",
                self.stagein_cwl_file,
                "--stageout",
                self.stageout_cwl_file,
                self.app_cwl_file + "#dnbr",
            ],
        )
        with open(self.expected_wrapped_cwl) as f:
            contents = f.read()
            assert result.output == contents

    def test_dNBR_invalid_hashtag(self):
        runner = CliRunner()
        result = runner.invoke(
            app.main,
            [
                "--stagein",
                self.stagein_cwl_file,
                "--stageout",
                self.stageout_cwl_file,
                self.app_cwl_file + "#invalidId",
            ],
        )
        assert result.exception.args[0] == "Wrong Workflow"

    def test_dNBR_empty_hashtag(self):
        runner = CliRunner()
        result = runner.invoke(
            app.main,
            [
                "--stagein",
                self.stagein_cwl_file,
                "--stageout",
                self.stageout_cwl_file,
                self.app_cwl_file + "#",
            ],
        )
        assert result.exception.args[0] == "No value after the hashtag was found."

    def test_programmatic_run(self):

        workflowId = "dnbr"
        cwl = f"{self.app_cwl_file}#{workflowId}"
        rulez = None
        output = self.temp_output_file.name
        # output = "ref.cwl"
        maincwl = None
        stagein = self.stagein_cwl_file
        stageout = self.stageout_cwl_file
        assets = None

        wf = Parser(
            cwl=cwl,
            output=output,
            stagein=stagein,
            stageout=stageout,
            maincwl=maincwl,
            rulez=rulez,
            assets=assets,
        )
        wf.write_output()

        a_file = open(self.temp_output_file.name)
        a_file.read()
        # print(f"##\n{file_contents}\n##")

        assert filecmp.cmp(self.temp_output_file.name, self.expected_wrapped_cwl)

    def test_programmatic_run_invalid_workflow_id(self):

        cwl = f"{self.app_cwl_file}"
        rulez = None
        output = self.temp_output_file.name
        maincwl = None
        stagein = self.stagein_cwl_file
        stageout = self.stageout_cwl_file
        assets = None

        try:
            wf = Parser(
                cwl=cwl,
                output=output,
                stagein=stagein,
                stageout=stageout,
                maincwl=maincwl,
                rulez=rulez,
                assets=assets,
            )
            wf.write_output()
        except ValueError as ve:
            assert str(ve) == "Wrong Workflow"

    @unittest.SkipTest
    def test_cwl_as_dict(self):

        workflowId = "dnbr"

        with open(self.app_cwl_file, "r") as stream:
            cwl = yaml.full_load(stream)

        rulez = None
        output = self.temp_output_file.name
        # output = "cwl.cwl"
        maincwl = None
        stagein = self.stagein_cwl_file
        stageout = self.stageout_cwl_file
        assets = None

        wf = Parser(
            cwl=cwl,
            output=output,
            stagein=stagein,
            stageout=stageout,
            maincwl=maincwl,
            rulez=rulez,
            assets=assets,
            workflow_id=workflowId,
        )
        wf.write_output()

        a_file = open(self.temp_output_file.name)
        a_file.read()
        # print(f"##\n{file_contents}\n##")

        assert filecmp.cmp(self.temp_output_file.name, self.expected_wrapped_cwl)
