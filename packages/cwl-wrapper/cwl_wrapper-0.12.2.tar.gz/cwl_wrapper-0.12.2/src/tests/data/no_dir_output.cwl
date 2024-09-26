cwlVersion: v1.0

$namespaces:
  s: https://schema.org/
s:softwareVersion: 0.5.0
schemas:
- http://schema.org/version/9.0/schemaorg-current-http.rdf


$graph:
- class: Workflow

  id: s1-snapping-ifg
  label: SNAPPING Interferograms
  doc: This service computes Interferograms for SNAPPING

  requirements:
  - class: SubworkflowFeatureRequirement
  - class: ScatterFeatureRequirement
  - class: InlineJavascriptRequirement
  - class: SubworkflowFeatureRequirement

  inputs:

    reference:
      type: Directory[]
      label: Reference SLC dataset
    secondary:
      type: Directory[]
      label: Secondary SLC dataset
    aoi:
      type: string
      label: Area of interest as WKT
      doc: Area of interest as WKT
    aoi_coreg:
      type: string
      label: Yes/No
      doc: Use all the AOI for the coregistration
    first_run:
      type: string
      label: Yes/No
      doc: first IFG in the stack
    pol:
      type: string
      default: VV
      label: selected polarisation
      doc: selected polarisation
    dem_name:
      type: string
      default: "SRTM 3Sec"
      label: DEM Name
      doc: DEM Name
    originator_uid:
      type: string?
      label: DI Identifier of the originator, coming from trigger queue
      doc: DI Identifier of the originator, coming from trigger queue
    stack_uuid:
      type: string
      label: Stack uuid
    _T2Username:
      type: string
      label: Terradue username
      doc: Terradue username
    _T2ApiKey:
      type: string
      label: Terradue API key
      doc: Terradue API key

  outputs:
  - id: s3_catalog_output
    outputSource:
    - node_post_processing/s3_catalog_output
    type: string

  steps:

    node_graphista:
      in:
        reference: reference
        secondary: secondary
        aoi: aoi
        aoi_coreg: aoi_coreg
        first_run: first_run
        dem: dem_name
      out:
      - insar

      run: "#graphista"

    node_post_processing:
      in:
        reference: reference
        secondary: secondary
        interferogram:
          source: node_graphista/insar
        first_run: first_run
        dem: dem_name
        username: _T2Username
        api_key: _T2ApiKey
        originator_uid: originator_uid
        stack_uuid: stack_uuid
      out:
      - s3_catalog_output

      run: "#post_processing"

- class: CommandLineTool

  id: graphista
  label: generates the snapping interferogram for S1 SLC

  requirements:
    DockerRequirement:
      dockerPull: docker.terradue.com/graphista:0.9.1
    ResourceRequirement:
      coresMax: 4
      ramMax: 36000
    InlineJavascriptRequirement: {}
    InitialWorkDirRequirement:
      listing:
        - entryname: custom.vmoptions
          entry: |-
            # Enter one VM parameter per line
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
            -XX:-UseGCOverheadLimit
        - entryname: run_me.sh
          entry: |-
            #!/bin/bash
            reference=$1

            mkdir -p /tmp/work
            cd /tmp/work

            graphista run "$@"

            cd -

            Stars copy -r 4 -rel -xa False -o ./ file:///tmp/work/catalog.json

            rm -fr .cache .config .install4j

  baseCommand: ["/bin/bash", "run_me.sh"]


  arguments:
  - --recipe
  - "s1-slc-insar-snapping"
  - valueFrom: |
      ${
        var references=[];
        for (var i = 0; i < inputs.reference.length; i++) {
          references.push("--reference");
          references.push(inputs.reference[i].path);
        }
        return references;
      }
  - valueFrom: |
      ${
        var secondaries=[];
        for (var i = 0; i < inputs.secondary.length; i++) {
          secondaries.push("--secondary");
          secondaries.push(inputs.secondary[i].path);
        }
        return secondaries;
      }
  - valueFrom: |
      ${ return ["--Subset", "geoRegion=" + inputs.aoi]; }
  - valueFrom: |
      ${ return ["--param", "aoi_coreg=" + inputs.aoi_coreg]; }
  - valueFrom: |
      ${ return ["--param", "first_run=" + inputs.first_run]; }
  - valueFrom: |
      ${ return ["--param", "dem=" + inputs.dem]; }

  inputs:
    reference:
      type: Directory[]
    secondary:
      type: Directory[]
    aoi:
      type: string
    aoi_coreg:
      type: string
    first_run:
      type: string
    dem:
      type: string

  outputs:
    insar:
      type: Directory
      outputBinding:
        glob: .

- class: CommandLineTool

  id: post_processing
  label: post processes the SNAPPING interferogram

  requirements:
    DockerRequirement:
      dockerPull: post_processing
    ResourceRequirement:
      coresMax: 2
      ramMax: 8000
    InlineJavascriptRequirement: {}
    EnvVarRequirement:
      envDef:
        PATH: /opt/conda/envs/env_calrissian/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
        PYTHONPATH: /app

  baseCommand: ["python", "-m", "app"]

  arguments:
  - valueFrom: |
      ${
        var references=[];
        for (var i = 0; i < inputs.reference.length; i++) {
          references.push("--reference");
          references.push(inputs.reference[i].path);
        }
        return references;
      }
  - valueFrom: |
      ${
        var secondaries=[];
        for (var i = 0; i < inputs.secondary.length; i++) {
          secondaries.push("--secondary");
          secondaries.push(inputs.secondary[i].path);
        }
        return secondaries;
      }
  - valueFrom: ${ return ["--interferogram", inputs.interferogram.path]; }
  - valueFrom: ${ return ["--first-run", inputs.first_run]; }
  - valueFrom: ${ return ["--dem", inputs.dem]; }
  - valueFrom: ${ return ["--username", inputs.username]; }
  - valueFrom: ${ return ["--api-key", inputs.api_key]; }
  - valueFrom: ${ return ["--first-run", inputs.first_run]; }
  - valueFrom: ${ return ["--stack-uuid", inputs.stack_uuid]; }
  - valueFrom: ${ if (inputs.originator_uid == null){
                  return ["--empty"]
                  } else {
                  return ["--originator", inputs.originator_uid];
                  }
                  }

  inputs:
    reference:
      type: Directory[]
    secondary:
      type: Directory[]
    interferogram:
      type: Directory
    first_run:
      type: string
    dem:
      type: string
    username:
      type: string
    api_key:
      type: string
    originator_uid:
      type: string?
    stack_uuid:
      type: string
    s3_bucket:
      type: string
      default: "gep-ifg-snapping-new"
  outputs:
    s3_catalog_output:
      outputBinding:
        outputEval: ${ return "s3://" + inputs.s3_bucket + "/" + inputs.username + "/" + inputs.stack_uuid + "/catalog.json"; }
      type: string
