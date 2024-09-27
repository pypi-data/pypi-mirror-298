import click
import click_config_file
from cwl_wrapper.parser import Parser


@click.command()
@click.option(
    "--output",
    "output",
    default="-",
    help="default main cel template assets/maincwl.yaml",
)
@click.option(
    "--stagein",
    "stagein",
    default=None,
    help="default stagein template assets/stagein.yaml",
)
@click.option(
    "--stageout",
    "stageout",
    default=None,
    help='default "stageout" template assets/stageout.yaml',
)
@click.option("--maincwl", "maincwl", default=None, help="default maincwl assets/maincwl.yaml")
@click.option("--rulez", "rulez", default=None, help="rules default file assets/rules.yaml")
@click.option(
    "--assets",
    "assets",
    default=None,
    help="use <value> as maincwl from assets/<values>",
)
@click.option(
    "--workflow-id",
    "workflow_id",
    default=None,
    help="workflow id",
)
@click.argument("cwl")
@click_config_file.configuration_option(
    "--conf",
    "-c",
    implicit=True,
    config_file_name="/home/jovyan/.cwlwrapper/default.conf",
    help="Read options from FILE instead of command line; "
    + "default file: /home/jovyan/.cwlwrapper/default.conf",
)
def main(cwl, output, stagein, stageout, maincwl, rulez, assets, workflow_id):
    """
    The cwl-parser
    """
    wf = Parser(
        cwl=cwl,
        output=output,
        stagein=stagein,
        stageout=stageout,
        maincwl=maincwl,
        rulez=rulez,
        assets=assets,
        workflow_id=workflow_id,
    )
    wf.write_output()


if __name__ == "__main__":
    main()
