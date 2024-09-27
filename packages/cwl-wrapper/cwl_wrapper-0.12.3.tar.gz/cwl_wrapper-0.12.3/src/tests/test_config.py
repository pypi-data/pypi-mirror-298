import os
import shutil
import unittest

from click.testing import CliRunner
from cwl_wrapper import app


class TestConfig(unittest.TestCase):
    def setUp(self):
        testdir = os.path.dirname(__file__)

        self.default_config_file = os.path.join(testdir, "data/default_config.conf")
        self.custom_config_file = os.path.join(testdir, "data/custom_config.conf")
        self.app_cwl_file = os.path.join(testdir, "data/dNBR.cwl")
        self.expected_config_default_cwl_file = os.path.join(
            testdir, "data/test_config_default_expected.cwl"
        )
        self.expected_config_custom_cwl_file = os.path.join(
            testdir, "data/test_config_custom_expected.cwl"
        )

        # Create default config file
        with open(self.default_config_file, "w") as f:
            print('stagein="{0}/data/stagein.cwl"'.format(testdir), file=f)
            print('stageout="{0}/data/stageout.cwl"'.format(testdir), file=f)

        # Create custom config file
        with open(self.custom_config_file, "w") as f:
            print('stagein="{0}/data/stagein.cwl"'.format(testdir), file=f)
            print('stageout="{0}/data/stageout_alt.cwl"'.format(testdir), file=f)

    def test_default_config(self):
        runner = CliRunner()
        result = runner.invoke(
            app.main,
            [
                self.app_cwl_file + "#dnbr",
            ],
        )
        print(result.output)

        with open(self.expected_config_default_cwl_file) as f:
            contents = f.read()
            assert result.output == contents

    def test_custom_config(self):
        runner = CliRunner()

        # Custom configuration uses a slightly modified stageout.cwl
        # for the stageout option
        result = runner.invoke(
            app.main,
            [
                "--conf",
                self.custom_config_file,
                self.app_cwl_file + "#dnbr",
            ],
        )
        print(result.output)

        with open(self.expected_config_custom_cwl_file) as f:
            contents = f.read()
            assert result.output == contents
