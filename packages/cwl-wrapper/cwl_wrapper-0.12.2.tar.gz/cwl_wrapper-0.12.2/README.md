[![Build Status](https://travis-ci.com/EOEPCA/cwl-wrapper.svg?branch=main)](https://travis-ci.com/EOEPCA/cwl-wrapper)

<br />
<p align="center">
  <a href="https://github.com/EOEPCA/cwl-wrapper">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">CWL-WRAPPER</h3>
  <p align="center">
    <br />
    <a href="https://eoepca.github.io/proc-ades/master/">Open Design</a>
    .
    <a href="https://github.com/EOEPCA/cwl-wrapper/issues">Report Bug</a>
    ·
    <a href="https://github.com/EOEPCA/cwl-wrapper/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

- [Table of Contents](#table-of-contents)
- [About The Project](#about-the-project)
- [Getting Started & Usage](#getting-started--usage)
  - [Installation](#Installation)
    - [Via conda](#via-conda)
    - [Development](#development)
    - [Requirements](#requirements)
    - [python requirements](#python-requirements)
  - [Configuration](#configuration)
    - [Rules](#rules)
  - [Usage](#Usage)
  - [Examples](#examples)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

## About The Project


<!-- GETTING STARTED -->
## Getting Started & Usage

### Installation

#### Via conda

```bash
conda install -c eoepca cwl-wrapper
```

#### Development

Clone this reposotory, then create the conda environment with:

```bash
cd cwl-wrapper
conda env create -f environment.yml
conda activate env_cwl_wrapper
```

Use setuptools to install the project:

```bash
python setup.py install
```

Check the installation with:

```bash
cwl-wrapper --help
```

#### Requirements

- Python
- console

#### Python requirements

- jinja2
- pyyaml
- click
- click-config-file

### Configuration

The rules, that establish connections and conventions with the user cwl, are defined in
[the cwl-wrapper configuration file](src/cwl_wrapper/assets/rules.yaml).

#### Rules

```yaml
rulez:
  version: 1
```

`rulez -> version` defines the Rules version. Currently only version 1 is managed

```yaml
parser:
  driver: cwl
```

`parser -> driver` defines the type of objects to be parsed

---

```yaml
onstage:
  driver: cwl

  stage_in:
    connection_node: node_stage_in
    if_scatter:
      scatterMethod: dotproduct

  on_stage:
    connection_node: on_stage

  stage_out:
    connection_node: node_stage_out
```

The `onstage` configuration is applied to `maincwl.yaml` file

`onstage -> driver` defines the driver to use during the translation: The result must be a `CWL` format

`onstage -> stage_in`

`onstage -> stage_in -> connection_node` defines the anchor node name for `stage-in` start. If the node does not exist, the parser creates it.

`onstage -> stage_in -> if_scatter` defines the conditions for `scatter` methods

`onstage -> stage_in -> if_scatter -> scatterMethod` is the method to use for scatter feature

`onstage -> on_stage`

`onstage -> on_stage -> connection_node`  defines the anchor node name for `user node`. If the node does not exist, the parser creates it.

`onstage -> stage_out -> connection_node` defines the anchor node name for `stage-out` start. If the node does not exist, the parser creates it.

The `stage_in`, `stage_out` and `on-stage` nodes can be customized by user.

The Parser uses the node name as an anchor to start the phase.

[Base template](src/cwl_wrapper/assets/maincwl.yaml) example

```yaml
class: Workflow
doc: Main stage manager
id: stage-manager
label: theStage
inputs: []
outputs: {}

requirements:
  SubworkflowFeatureRequirement: {}
  ScatterFeatureRequirement: {}
```

---

```yaml
output:
  driver: cwl
  name: '-'
  type: $graph
```

`output -> driver` defines the output driver, currently is defined only 'CWL' driver

`output -> name` this parameter is deprecated

`output -> type` defines the type of output

* `$graph` if driver is `CWL` the output will be in one file using
[`$graph` entry point](https://www.commonwl.org/v1.1/SchemaSalad.html#Document_graph)

Driver `CWL` needs the [templates to define the types](src/cwl_wrapper/assets/rules.yaml#L35-L75):

```yaml
  GlobalInput:
    Directory: string
    Directory[]: string[]
```

defines the rules to replace the elements from user type to WPS type.
example:
[user workflow](assets/vegetation.cwl#L40-L47) changes in

* [workflow input](assets/vegetation.wf.yaml#L11-L16)
* [on-stage-parameters-in](assets/vegetation.wf.yaml#L188-L189)

---

```yaml
  stage_in:
    Directory:
      type: string
      inputBinding:
        position: 2

    Directory[]:
      type: string[]
      inputBinding:
        position: 2
```

are the templates to link the user inputs
example
* [node_stage_in->input_reference](assets/vegetation.wf.yaml#L70-L73)
* [node_stage_in_1->input_reference2](assets/vegetation.wf.yaml#L103-L106)

---

```yaml
  stage_out:
    Directory:
      type: Directory
      inputBinding:
        position: 6

    Directory[]:
      type: Directory[]
      inputBinding:
        position: 6
```

defines the template of [stage-output](assets/vegetation.wf.yaml#L171-L174)
and depends from the user output type

### Usage

The cwl-wrapper requires
* user CWL
*

### Examples

In this section we will study how to create and change cwl-wrapper templates:

* src/cwl_wrapper/assets/stagein.yaml
* src/cwl_wrapper/assets/stageout.yaml
* src/cwl_wrapper/assets/maincwl.yaml

#### [vegetation.cwl](assets/vegetation.cwl)

Default run

```yaml
$graph:
  - baseCommand: vegetation-index
    class: CommandLineTool
    hints:
      DockerRequirement:
        dockerPull: eoepca/vegetation-index:0.2
    id: clt
    inputs:
      inp1:
        inputBinding:
          position: 1
          prefix: --input_reference
        type: Directory
      inp2:
        inputBinding:
          position: 2
          prefix: --aoi
        type: string
    outputs:
      results:
        outputBinding:
          glob: .
        type: Directory
    requirements:
      EnvVarRequirement:
        envDef:
          PATH: /opt/anaconda/envs/env_vi/bin:/opt/anaconda/envs/env_vi/bin:/home/fbrito/.nvm/versions/node/v10.21.0/bin:/opt/anaconda/envs/notebook/bin:/opt/anaconda/bin:/usr/share/java/maven/bin:/opt/anaconda/bin:/opt/anaconda/envs/notebook/bin:/opt/anaconda/bin:/usr/share/java/maven/bin:/opt/anaconda/bin:/opt/anaconda/condabin:/opt/anaconda/envs/notebook/bin:/opt/anaconda/bin:/usr/lib64/qt-3.3/bin:/usr/share/java/maven/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/fbrito/.local/bin:/home/fbrito/bin:/home/fbrito/.local/bin:/home/fbrito/bin
          PREFIX: /opt/anaconda/envs/env_vi
      ResourceRequirement: {}
    stderr: std.err
    stdout: std.out
  - class: Workflow
    doc: Vegetation index processor, the greatest
    id: vegetation-index
    inputs:
      aoi:
        doc: Area of interest in WKT
        label: Area of interest
        type: string
      input_reference:
        doc: EO product for vegetation index
        label: EO product for vegetation index
        type: Directory[]
      input_reference2:
        doc: EO product for vegetation index
        label: EO product for vegetation index
        type: Directory[]
    label: Vegetation index
    outputs:
      - id: wf_outputs
        outputSource:
          - node_1/results
        type:
          items: Directory
          type: array
    requirements:
      - class: ScatterFeatureRequirement
    steps:
      node_1:
        in:
          inp1: input_reference
          inp2: aoi
        out:
          - results
        run: '#clt'
        scatter: inp1
        scatterMethod: dotproduct
cwlVersion: v1.0
```

```shell script
python cwl-wrapper assets/vegetation.cwl  --output  assets/vegetation.wf.yaml
```

expected result is the file [vegetation.wf.yaml](assets/vegetation.wf.yaml)

In the new file, have been added the elements:

* [General workflow](assets/vegetation.wf.yaml#L1)
    * [node_stage_in... node_stage_in_x](assets/vegetation.wf.yaml#L53-L118)
    * [on_stage](assets/vegetation.wf.yaml#L185-192)
    * [node_stage_out](assets/vegetation.wf.yaml#L119-184)
* [User CommandLineTool/vegetation-index](assets/vegetation.wf.yaml#L193-222)
* [User Workflow](assets/vegetation.wf.yaml#L223-L258)


##### New [Stage-in](src/cwl_wrapper/assets/stagein.yaml)

In the new [stage-in](assets/stagein-test.cwl) we are going to add two new parameters

* parameter_A
* paraneter_B

```yaml
baseCommand: stage-in
class: CommandLineTool
hints:
  DockerRequirement:
    dockerPull: eoepca/stage-in:0.2
id: stagein
arguments:
  - prefix: -t
    position: 1
    valueFrom: "./"

inputs:
    parameter_A:
      doc: EO product for vegetation index
      label: EO product for vegetation index
      type: string[]
    parameter_B:
      doc: EO product for vegetation index
      label: EO product for vegetation index
      type: string[]
outputs: {}
requirements:
  EnvVarRequirement:
    envDef:
      PATH: /opt/anaconda/envs/env_stagein/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
  ResourceRequirement: {}
```

> the inputs can be written in Dict or List format

In the new run, we have to update the parameter `stagein`:

```shell script
python cwl-wrapper assets/vegetation.cwl  --stagein assets/stagein-test.cwl --output  vegetation.wf_new_stagein.yaml
```

In the new output file [vegetation.wf_new_stagein.yaml](assets/vegetation.wf_new_stagein.yaml) have been added:

* New user template
* In the general workflow:
    * [parameter_A](assets/vegetation.wf_new_stagein.yaml#L29-L32)
    * [parameter_B](assets/vegetation.wf_new_stagein.yaml#L33-L36)
* node_stage_in -> in -> [parameters](assets/vegetation.wf_new_stagein.yaml#L64-L65)
* node_stage_in_1 -> in -> [parameters](assets/vegetation.wf_new_stagein.yaml#L107-L108)

##### New [Stage-out](src/cwl_wrapper/assets/stageout.yaml)

The Stage-out template responds at the same rules of stage-in template, we only need to change the run parameters

```shell script
python cwl-wrapper assets/vegetation.cwl  --stageout assets/stagein-test.cwl --output  vegetation.wf_new_stageout.yaml
```

##### New [maincwl.yaml](src/cwl_wrapper/assets/rules.yaml)

The [maincwl.yaml](src/cwl_wrapper/assets/rules.yaml) is the workflow where the cwl-wrapper pastes
all the user templates creating a new cwl workflow

maincwl.yaml works with the [rules file](src/cwl_wrapper/assets/rules.yaml) where are defined the connection rules

In [rules file](src/cwl_wrapper/assets/rules.yaml) are defined three entry points which they'll created or will linked to
new workflow:

* [stage-in](src/cwl_wrapper/assets/rules.yaml#L11-L12)
* [onstage](src/cwl_wrapper/assets/rules.yaml#L19-L20)
* [stage-out](src/cwl_wrapper/assets/rules.yaml#L22-L23)


Now we can try to change the maincwl.yaml adding a new custom step before the stage-in

```yaml
class: Workflow
doc: Main stage manager
id: stage-manager
label: theStage
inputs:
  myinputs:
      doc: myinputs doc
      label: myinputs label
      type: string
outputs: {}
requirements:
  SubworkflowFeatureRequirement: {}
  ScatterFeatureRequirement: {}
steps:
    custom_node:
      in:
        myinputs: myinputs
      out:
      - example_out
      run:
        class: CommandLineTool
        baseCommand: do_something
        inputs:
          myinputs:
            type: string
            inputBinding:
              prefix: --file
        outputs:
          example_out:
            type: File
            outputBinding:
              glob: hello.txt
    node_stage_in:
      in:
        custom_input: custom_node/example_out
      out: []
      run: ''
```

Run

```shell script
python cwl-wrapper assets/vegetation.cwl  --maincwl  ../assets/custom_main.cwl --output  vegetation.wf.custom_maincwl.yaml
```

The output file [vegetation.wf.custom_maincwl.yaml](assets/vegetation.wf.custom_maincwl.yaml)

* [General inputs](assets/vegetation.wf.custom_maincwl.yaml#L25-L28)
* [node_stage_in](assets/vegetation.wf.custom_maincwl.yaml#L77) link


<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/EOEPCA/proc-ades/issues) for a list of proposed features (and known issues).

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create.
Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## License

Distributed under the Apache-2.0 License. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

Terradue - [@terradue](https://twitter.com/terradue) - info@terradue.com

Project Link: [https://github.com/EOEPCA/proc-ades](https://github.com/EOEPCA/proc-ades)

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* README.md is based on [this template](https://github.com/othneildrew/Best-README-Template) by
[Othneil Drew](https://github.com/othneildrew).

## Try me on Binder

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/EOEPCA/cwl-wrapper/develop)
