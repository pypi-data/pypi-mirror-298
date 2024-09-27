$graph:
- baseCommand: iris-change-detection
  class: CommandLineTool
  hints:
    DockerRequirement:
      dockerPull: docker.terradue.com/iris-change-detection:dev0.5.9
  id: clt
  inputs:
    pre_event:
      inputBinding:
        position: 1
        prefix: --pre-event
      type: Directory
    post_event:
      inputBinding:
        position: 2
        prefix: --post-event
      type: Directory
    mask:
      inputBinding:
        position: 3
        prefix: --mask
      type: Directory?
    win_size:
      inputBinding:
        position: 4
        prefix: --win_size
      type: string
    threshold:
      inputBinding:
        position: 5
        prefix: --threshold
      type: string
    coreg_type:
      inputBinding:
        position: 6
        prefix: --coregistration
      type:
      - symbols:
        - None
        - Rigid
        - Elastic
        type: enum
    aoi:
      inputBinding:
        position: 7
        prefix: --aoi
      type: string?
  outputs:
    results:
      outputBinding:
        glob: .
      type: Directory
  requirements:
    EnvVarRequirement:
      envDef:
        APP_DOCKER_IMAGE: docker.terradue.com/iris-change-detection:dev0.5.9
        APP_NAME: iris-change-detection
        APP_PACKAGE: app-iris-change-detection.dev.0.5.9
        APP_VERSION: 0.5.9
        PATH: /srv/conda/envs/env_iris_change_detection/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/srv/conda/envs/env_iris_change_detection/bin
        _PROJECT: CPE
    ResourceRequirement: {}
  stderr: std.err
  stdout: std.out
- class: Workflow
  doc: This service performs a Change Detection using a pair of calibrated optical
    or SAR single band assets acquired from the same sensor. The output consists of
    multiple change detection products derived from the Structural Similarity Index
    that show intensity, extent, and contours of the detected changes in the region
    of interest
  id: iris-change-detection
  inputs:
    pre_event:
      doc: Pre-event calibrated single band asset path
      label: Pre-event calibrated single band asset path
      type: Directory
    post_event:
      doc: Post-event calibrated single band asset path
      label: Post-event calibrated single band asset path
      type: Directory
    mask:
      doc: Optional mask
      label: Optional mask
      type: Directory?
    win_size:
      default: '41'
      doc: Size, in pixels, of the sliding window used to detect changes, bigger values
        produce smoother results
      label: Size, in pixels, of the sliding window used to detect changes, bigger
        values produce smoother results
      type: string
    threshold:
      default: '0.4'
      doc: Threshold value, between 0 and 1, for the detected change contouring
      label: Threshold value, between 0 and 1, for the detected change contouring
      type: string
    coreg_type:
      default: Rigid
      doc: Coregistration type
      label: Coregistration type
      type:
      - symbols:
        - None
        - Rigid
        - Elastic
        type: enum
    aoi:
      doc: Area of interest in Well-known Text (WKT)
      label: Area of interest in Well-known Text (WKT)
      type: string?
  label: Change Detection Analysis (IRIS)
  outputs:
  - id: wf_outputs
    outputSource:
    - step_1/results
    type: Directory
  steps:
    step_1:
      in:
        pre_event: pre_event
        post_event: post_event
        mask: mask
        win_size: win_size
        threshold: threshold
        coreg_type: coreg_type
        aoi: aoi
      out:
      - results
      run: '#clt'
$namespaces:
  s: https://schema.org/
cwlVersion: v1.0
s:softwareVersion: 0.5.9
schemas:
- http://schema.org/version/9.0/schemaorg-current-http.rdf
