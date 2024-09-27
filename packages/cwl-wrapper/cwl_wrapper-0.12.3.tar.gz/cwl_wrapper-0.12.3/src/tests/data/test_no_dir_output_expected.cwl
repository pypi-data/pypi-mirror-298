$graph:
- $namespaces:
    cwltool: http://commonwl.org/cwltool#
  class: Workflow
  doc: Main stage manager
  hints:
    cwltool:Secrets:
      secrets:
      - ADES_STAGEIN_AWS_SERVICEURL
      - ADES_STAGEIN_AWS_ACCESS_KEY_ID
      - ADES_STAGEIN_AWS_SECRET_ACCESS_KEY
      - ADES_STAGEOUT_AWS_SERVICEURL
      - ADES_STAGEOUT_AWS_ACCESS_KEY_ID
      - ADES_STAGEOUT_AWS_SECRET_ACCESS_KEY
  id: main
  inputs:
    ADES_STAGEIN_AWS_ACCESS_KEY_ID:
      type: string?
    ADES_STAGEIN_AWS_REGION:
      type: string?
    ADES_STAGEIN_AWS_SECRET_ACCESS_KEY:
      type: string?
    ADES_STAGEIN_AWS_SERVICEURL:
      type: string?
    ADES_STAGEOUT_AWS_ACCESS_KEY_ID:
      type: string?
    ADES_STAGEOUT_AWS_REGION:
      type: string?
    ADES_STAGEOUT_AWS_SECRET_ACCESS_KEY:
      type: string?
    ADES_STAGEOUT_AWS_SERVICEURL:
      type: string?
    ADES_STAGEOUT_OUTPUT:
      type: string?
    _T2ApiKey:
      doc: Terradue API key
      id: _T2ApiKey
      label: Terradue API key
      type: string
    _T2Username:
      doc: Terradue username
      id: _T2Username
      label: Terradue username
      type: string
    aoi:
      doc: Area of interest as WKT
      id: aoi
      label: Area of interest as WKT
      type: string
    aoi_coreg:
      doc: Use all the AOI for the coregistration
      id: aoi_coreg
      label: Yes/No
      type: string
    dem_name:
      default: SRTM 3Sec
      doc: DEM Name
      id: dem_name
      label: DEM Name
      type: string
    first_run:
      doc: first IFG in the stack
      id: first_run
      label: Yes/No
      type: string
    originator_uid:
      doc: DI Identifier of the originator, coming from trigger queue
      id: originator_uid
      label: DI Identifier of the originator, coming from trigger queue
      type: string?
    pol:
      default: VV
      doc: selected polarisation
      id: pol
      label: selected polarisation
      type: string
    process:
      type: string
    reference:
      id: reference
      label: Reference SLC dataset
      type: string[]
    secondary:
      id: secondary
      label: Secondary SLC dataset
      type: string[]
    stack_uuid:
      id: stack_uuid
      label: Stack uuid
      type: string
  label: macro-cwl
  outputs:
    s3_catalog_output:
      outputSource:
      - on_stage/s3_catalog_output
      type: string
  requirements:
    InlineJavascriptRequirement: {}
    ScatterFeatureRequirement: {}
    SubworkflowFeatureRequirement: {}
  steps:
    node_stage_in:
      in:
        ADES_STAGEIN_AWS_ACCESS_KEY_ID: ADES_STAGEIN_AWS_ACCESS_KEY_ID
        ADES_STAGEIN_AWS_REGION: ADES_STAGEIN_AWS_REGION
        ADES_STAGEIN_AWS_SECRET_ACCESS_KEY: ADES_STAGEIN_AWS_SECRET_ACCESS_KEY
        ADES_STAGEIN_AWS_SERVICEURL: ADES_STAGEIN_AWS_SERVICEURL
        input: reference
      out:
      - reference_out
      run:
        baseCommand:
        - /bin/bash
        - stagein.sh
        class: CommandLineTool
        cwlVersion: v1.0
        doc: Run Stars for staging input data
        hints:
          DockerRequirement:
            dockerPull: terradue/stars:2.9.2
          cwltool:Secrets:
            secrets:
            - ADES_STAGEIN_AWS_SERVICEURL
            - ADES_STAGEIN_AWS_ACCESS_KEY_ID
            - ADES_STAGEIN_AWS_SECRET_ACCESS_KEY
        id: stars
        inputs:
          ADES_STAGEIN_AWS_ACCESS_KEY_ID:
            type: string?
          ADES_STAGEIN_AWS_REGION:
            type: string?
          ADES_STAGEIN_AWS_SECRET_ACCESS_KEY:
            type: string?
          ADES_STAGEIN_AWS_SERVICEURL:
            type: string?
          input:
            type: string?
        outputs:
          reference_out:
            outputBinding:
              glob: .
            type: Directory
        requirements:
          EnvVarRequirement:
            envDef:
              AWS_ACCESS_KEY_ID: $(inputs.ADES_STAGEIN_AWS_ACCESS_KEY_ID)
              AWS_SECRET_ACCESS_KEY: $(inputs.ADES_STAGEIN_AWS_SECRET_ACCESS_KEY)
              AWS__AuthenticationRegion: $(inputs.ADES_STAGEIN_AWS_REGION)
              AWS__Region: $(inputs.ADES_STAGEIN_AWS_REGION)
              AWS__ServiceURL: $(inputs.ADES_STAGEIN_AWS_SERVICEURL)
              PATH: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
          InitialWorkDirRequirement:
            listing:
            - entry: "#!/bin/bash\n  set -x\n  res=0\n  input='$( inputs.input )'\n\
                \n  [ \"\\${input}\" != \"null\" ] && {\n\n    IFS='#' read -r -a\
                \ reference <<< '$( inputs.input )'\n    input_len=\\${#reference[@]}\n\
                \n    [[ \\${input_len} == 2 ]] && {\n\n        IFS=',' read -r -a\
                \ assets <<< \\${reference[1]}\n        af=\" \"\n        for asset\
                \ in \\${assets[@]}\n        do\n          af=\"\\${af} -af \\${asset}\"\
                \n        done\n    } || {\n      af=\"--empty\"\n    }\n    Stars\
                \ copy -v -rel -r '4' \\${af} -o ./ \\${reference[0]}\n    res=$?\n\
                \  }\n  rm -fr stagein.sh\n  exit \\${res}"
              entryname: stagein.sh
          InlineJavascriptRequirement: {}
          ResourceRequirement: {}
      scatter: input
      scatterMethod: dotproduct
    node_stage_in_1:
      in:
        ADES_STAGEIN_AWS_ACCESS_KEY_ID: ADES_STAGEIN_AWS_ACCESS_KEY_ID
        ADES_STAGEIN_AWS_REGION: ADES_STAGEIN_AWS_REGION
        ADES_STAGEIN_AWS_SECRET_ACCESS_KEY: ADES_STAGEIN_AWS_SECRET_ACCESS_KEY
        ADES_STAGEIN_AWS_SERVICEURL: ADES_STAGEIN_AWS_SERVICEURL
        input: secondary
      out:
      - secondary_out
      run:
        baseCommand:
        - /bin/bash
        - stagein.sh
        class: CommandLineTool
        cwlVersion: v1.0
        doc: Run Stars for staging input data
        hints:
          DockerRequirement:
            dockerPull: terradue/stars:2.9.2
          cwltool:Secrets:
            secrets:
            - ADES_STAGEIN_AWS_SERVICEURL
            - ADES_STAGEIN_AWS_ACCESS_KEY_ID
            - ADES_STAGEIN_AWS_SECRET_ACCESS_KEY
        id: stars
        inputs:
          ADES_STAGEIN_AWS_ACCESS_KEY_ID:
            type: string?
          ADES_STAGEIN_AWS_REGION:
            type: string?
          ADES_STAGEIN_AWS_SECRET_ACCESS_KEY:
            type: string?
          ADES_STAGEIN_AWS_SERVICEURL:
            type: string?
          input:
            type: string?
        outputs:
          secondary_out:
            outputBinding:
              glob: .
            type: Directory
        requirements:
          EnvVarRequirement:
            envDef:
              AWS_ACCESS_KEY_ID: $(inputs.ADES_STAGEIN_AWS_ACCESS_KEY_ID)
              AWS_SECRET_ACCESS_KEY: $(inputs.ADES_STAGEIN_AWS_SECRET_ACCESS_KEY)
              AWS__AuthenticationRegion: $(inputs.ADES_STAGEIN_AWS_REGION)
              AWS__Region: $(inputs.ADES_STAGEIN_AWS_REGION)
              AWS__ServiceURL: $(inputs.ADES_STAGEIN_AWS_SERVICEURL)
              PATH: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
          InitialWorkDirRequirement:
            listing:
            - entry: "#!/bin/bash\n  set -x\n  res=0\n  input='$( inputs.input )'\n\
                \n  [ \"\\${input}\" != \"null\" ] && {\n\n    IFS='#' read -r -a\
                \ reference <<< '$( inputs.input )'\n    input_len=\\${#reference[@]}\n\
                \n    [[ \\${input_len} == 2 ]] && {\n\n        IFS=',' read -r -a\
                \ assets <<< \\${reference[1]}\n        af=\" \"\n        for asset\
                \ in \\${assets[@]}\n        do\n          af=\"\\${af} -af \\${asset}\"\
                \n        done\n    } || {\n      af=\"--empty\"\n    }\n    Stars\
                \ copy -v -rel -r '4' \\${af} -o ./ \\${reference[0]}\n    res=$?\n\
                \  }\n  rm -fr stagein.sh\n  exit \\${res}"
              entryname: stagein.sh
          InlineJavascriptRequirement: {}
          ResourceRequirement: {}
      scatter: input
      scatterMethod: dotproduct
    on_stage:
      in:
        _T2ApiKey: _T2ApiKey
        _T2Username: _T2Username
        aoi: aoi
        aoi_coreg: aoi_coreg
        dem_name: dem_name
        first_run: first_run
        originator_uid: originator_uid
        pol: pol
        reference: node_stage_in/reference_out
        secondary: node_stage_in_1/secondary_out
        stack_uuid: stack_uuid
      out:
      - s3_catalog_output
      run: '#s1-snapping-ifg'
- class: Workflow
  doc: This service computes Interferograms for SNAPPING
  id: s1-snapping-ifg
  inputs:
    _T2ApiKey:
      doc: Terradue API key
      label: Terradue API key
      type: string
    _T2Username:
      doc: Terradue username
      label: Terradue username
      type: string
    aoi:
      doc: Area of interest as WKT
      label: Area of interest as WKT
      type: string
    aoi_coreg:
      doc: Use all the AOI for the coregistration
      label: Yes/No
      type: string
    dem_name:
      default: SRTM 3Sec
      doc: DEM Name
      label: DEM Name
      type: string
    first_run:
      doc: first IFG in the stack
      label: Yes/No
      type: string
    originator_uid:
      doc: DI Identifier of the originator, coming from trigger queue
      label: DI Identifier of the originator, coming from trigger queue
      type: string?
    pol:
      default: VV
      doc: selected polarisation
      label: selected polarisation
      type: string
    reference:
      label: Reference SLC dataset
      type: Directory[]
    secondary:
      label: Secondary SLC dataset
      type: Directory[]
    stack_uuid:
      label: Stack uuid
      type: string
  label: SNAPPING Interferograms
  outputs:
  - id: s3_catalog_output
    outputSource:
    - node_post_processing/s3_catalog_output
    type: string
  requirements:
  - class: SubworkflowFeatureRequirement
  - class: ScatterFeatureRequirement
  - class: InlineJavascriptRequirement
  - class: SubworkflowFeatureRequirement
  steps:
    node_graphista:
      in:
        aoi: aoi
        aoi_coreg: aoi_coreg
        dem: dem_name
        first_run: first_run
        reference: reference
        secondary: secondary
      out:
      - insar
      run: '#graphista'
    node_post_processing:
      in:
        api_key: _T2ApiKey
        dem: dem_name
        first_run: first_run
        interferogram:
          source: node_graphista/insar
        originator_uid: originator_uid
        reference: reference
        secondary: secondary
        stack_uuid: stack_uuid
        username: _T2Username
      out:
      - s3_catalog_output
      run: '#post_processing'
- arguments:
  - --recipe
  - s1-slc-insar-snapping
  - valueFrom: "${\n  var references=[];\n  for (var i = 0; i < inputs.reference.length;\
      \ i++) {\n    references.push(\"--reference\");\n    references.push(inputs.reference[i].path);\n\
      \  }\n  return references;\n}\n"
  - valueFrom: "${\n  var secondaries=[];\n  for (var i = 0; i < inputs.secondary.length;\
      \ i++) {\n    secondaries.push(\"--secondary\");\n    secondaries.push(inputs.secondary[i].path);\n\
      \  }\n  return secondaries;\n}\n"
  - valueFrom: '${ return ["--Subset", "geoRegion=" + inputs.aoi]; }

      '
  - valueFrom: '${ return ["--param", "aoi_coreg=" + inputs.aoi_coreg]; }

      '
  - valueFrom: '${ return ["--param", "first_run=" + inputs.first_run]; }

      '
  - valueFrom: '${ return ["--param", "dem=" + inputs.dem]; }

      '
  baseCommand:
  - /bin/bash
  - run_me.sh
  class: CommandLineTool
  id: graphista
  inputs:
    aoi:
      type: string
    aoi_coreg:
      type: string
    dem:
      type: string
    first_run:
      type: string
    reference:
      type: Directory[]
    secondary:
      type: Directory[]
  label: generates the snapping interferogram for S1 SLC
  outputs:
    insar:
      outputBinding:
        glob: .
      type: Directory
  requirements:
    DockerRequirement:
      dockerPull: docker.terradue.com/graphista:0.9.1
    InitialWorkDirRequirement:
      listing:
      - entry: '# Enter one VM parameter per line

          # Initial memory allocation

          -Xms16G

          # Maximum memory allocation

          -Xmx32G

          # Disable verifier

          -Xverify:none

          # Turns on point performance optimizations

          -XX:+AggressiveOpts

          # disable some drawing driver useless in server mode

          -Dsun.java2d.noddraw=true

          -Dsun.awt.nopixfmt=true

          -Dsun.java2d.dpiaware=false

          # larger tile size to reduce I/O and GC

          -Dsnap.jai.defaultTileSize=1024

          -Dsnap.dataio.reader.tileWidth=1024

          -Dsnap.dataio.reader.tileHeigh=1024

          # disable garbage collector overhead limit

          -XX:-UseGCOverheadLimit'
        entryname: custom.vmoptions
      - entry: '#!/bin/bash

          reference=$1


          mkdir -p /tmp/work

          cd /tmp/work


          graphista run "$@"


          cd -


          Stars copy -r 4 -rel -xa False -o ./ file:///tmp/work/catalog.json


          rm -fr .cache .config .install4j'
        entryname: run_me.sh
    InlineJavascriptRequirement: {}
    ResourceRequirement:
      coresMax: 4
      ramMax: 36000
- arguments:
  - valueFrom: "${\n  var references=[];\n  for (var i = 0; i < inputs.reference.length;\
      \ i++) {\n    references.push(\"--reference\");\n    references.push(inputs.reference[i].path);\n\
      \  }\n  return references;\n}\n"
  - valueFrom: "${\n  var secondaries=[];\n  for (var i = 0; i < inputs.secondary.length;\
      \ i++) {\n    secondaries.push(\"--secondary\");\n    secondaries.push(inputs.secondary[i].path);\n\
      \  }\n  return secondaries;\n}\n"
  - valueFrom: ${ return ["--interferogram", inputs.interferogram.path]; }
  - valueFrom: ${ return ["--first-run", inputs.first_run]; }
  - valueFrom: ${ return ["--dem", inputs.dem]; }
  - valueFrom: ${ return ["--username", inputs.username]; }
  - valueFrom: ${ return ["--api-key", inputs.api_key]; }
  - valueFrom: ${ return ["--first-run", inputs.first_run]; }
  - valueFrom: ${ return ["--stack-uuid", inputs.stack_uuid]; }
  - valueFrom: ${ if (inputs.originator_uid == null){ return ["--empty"] } else {
      return ["--originator", inputs.originator_uid]; } }
  baseCommand:
  - python
  - -m
  - app
  class: CommandLineTool
  id: post_processing
  inputs:
    api_key:
      type: string
    dem:
      type: string
    first_run:
      type: string
    interferogram:
      type: Directory
    originator_uid:
      type: string?
    reference:
      type: Directory[]
    s3_bucket:
      default: gep-ifg-snapping-new
      type: string
    secondary:
      type: Directory[]
    stack_uuid:
      type: string
    username:
      type: string
  label: post processes the SNAPPING interferogram
  outputs:
    s3_catalog_output:
      outputBinding:
        outputEval: ${ return "s3://" + inputs.s3_bucket + "/" + inputs.username +
          "/" + inputs.stack_uuid + "/catalog.json"; }
      type: string
  requirements:
    DockerRequirement:
      dockerPull: post_processing
    EnvVarRequirement:
      envDef:
        PATH: /opt/conda/envs/env_calrissian/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
        PYTHONPATH: /app
    InlineJavascriptRequirement: {}
    ResourceRequirement:
      coresMax: 2
      ramMax: 8000
$namespaces:
  s: https://schema.org/
cwlVersion: v1.0
s:softwareVersion: 0.5.0
schemas:
- http://schema.org/version/9.0/schemaorg-current-http.rdf
