class: Workflow
$namespaces:
  cwltool: http://commonwl.org/cwltool#

doc: Main stage manager
id: main
label: macro-cwl
inputs: {}
outputs: {}
hints:
  "cwltool:Secrets":
    secrets: []
requirements:
  SubworkflowFeatureRequirement: {}
  ScatterFeatureRequirement: {}
  InlineJavascriptRequirement: {}


#steps:
#  node_stage_in:
#    in: {}
#    out: []
#    run: ''
##
#  on_stage:
#    in: {}
#    out: []
#    run: ''
#
#  node_stage_out:
#    in: {}
#    out: []
#    run: ''
