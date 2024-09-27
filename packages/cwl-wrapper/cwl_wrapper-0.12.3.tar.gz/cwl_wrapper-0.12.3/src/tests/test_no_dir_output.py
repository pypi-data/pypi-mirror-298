import os
import tempfile
import unittest

from click.testing import CliRunner
from cwl_wrapper import app


class TestNoDirOutputCwl(unittest.TestCase):
    def setUp(self):
        self.stagein_cwl_file = os.path.join(os.path.dirname(__file__), "data/stagein.cwl")
        self.stageout_cwl_file = os.path.join(os.path.dirname(__file__), "data/stageout.cwl")
        self.main_cwl_file = os.path.join(os.path.dirname(__file__), "data/main.cwl")

        self.app_cwl_file = os.path.join(os.path.dirname(__file__), "data/no_dir_output.cwl")
        self.expected_wrapped_cwl = os.path.join(
            os.path.dirname(__file__), "data/test_no_dir_output_expected.cwl"
        )
        self.expected_usage_test = os.path.join(os.path.dirname(__file__), "data/test_help_expected.txt")
        self.temp_output_file = tempfile.NamedTemporaryFile()

    def test_no_dir_output(self):
        runner = CliRunner()
        result = runner.invoke(
            app.main,
            [
                "--maincwl",
                self.main_cwl_file,
                "--stagein",
                self.stagein_cwl_file,
                "--stageout",
                self.stageout_cwl_file,
                self.app_cwl_file + "#s1-snapping-ifg",
            ],
        )
        print(result.output)

        with open(self.expected_wrapped_cwl) as f:
            contents = f.read()
            assert result.output == contents
