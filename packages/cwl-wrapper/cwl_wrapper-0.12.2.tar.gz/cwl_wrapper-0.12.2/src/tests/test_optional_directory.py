import os
import tempfile
import unittest

from click.testing import CliRunner
from cwl_wrapper import app


class TestOptionalDirectory(unittest.TestCase):
    def setUp(self):
        self.stagein_cwl_file = os.path.join(os.path.dirname(__file__), "data/stagein.cwl")
        self.stageout_cwl_file = os.path.join(os.path.dirname(__file__), "data/stageout.cwl")
        self.main_cwl_file = os.path.join(os.path.dirname(__file__), "data/main.cwl")
        self.rules_file = os.path.join(os.path.dirname(__file__), "data/rules.cwl")
        self.app_cwl_file = os.path.join(os.path.dirname(__file__), "data/test_optional_directory.cwl")
        self.expected_wrapped_cwl = os.path.join(
            os.path.dirname(__file__), "data/test_optional_directory_expected.cwl"
        )
        self.temp_output_file = tempfile.NamedTemporaryFile()

    def test_optional_directory(self):
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
                "--rulez",
                self.rules_file,
                self.app_cwl_file + "#iris-change-detection",
            ],
        )

        with open(self.expected_wrapped_cwl) as f:
            contents = f.read()
            print(result.output)
            assert result.output == contents
