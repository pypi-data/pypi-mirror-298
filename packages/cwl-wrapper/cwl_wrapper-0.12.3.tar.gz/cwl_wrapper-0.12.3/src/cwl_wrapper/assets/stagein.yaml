cwlVersion: v1.0
doc: "Run Stars for staging input data"
class: CommandLineTool
hints:
  DockerRequirement:
    dockerPull: terradue/stars:2.9.2
  "cwltool:Secrets":
    secrets:
    - ADES_STAGEIN_AWS_SERVICEURL
    - ADES_STAGEIN_AWS_ACCESS_KEY_ID
    - ADES_STAGEIN_AWS_SECRET_ACCESS_KEY
id: stars
requirements:
  EnvVarRequirement:
    envDef:
      PATH: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
      AWS__ServiceURL: $(inputs.ADES_STAGEIN_AWS_SERVICEURL)
      AWS__Region: $(inputs.ADES_STAGEIN_AWS_REGION)
      AWS__AuthenticationRegion: $(inputs.ADES_STAGEIN_AWS_REGION)
      AWS_ACCESS_KEY_ID: $(inputs.ADES_STAGEIN_AWS_ACCESS_KEY_ID)
      AWS_SECRET_ACCESS_KEY: $(inputs.ADES_STAGEIN_AWS_SECRET_ACCESS_KEY)
  ResourceRequirement: {}
  InlineJavascriptRequirement: {}
  InitialWorkDirRequirement:
        listing:
        - entryname: stagein.sh
          entry: |-
            #!/bin/bash
              set -x
              res=0
              input='$( inputs.input )'

              [ "\${input}" != "null" ] && {

                IFS='#' read -r -a reference <<< '$( inputs.input )'
                input_len=\${#reference[@]}

                [[ \${input_len} == 2 ]] && {

                    IFS=',' read -r -a assets <<< \${reference[1]}
                    af=" "
                    for asset in \${assets[@]}
                    do
                      af="\${af} -af \${asset}"
                    done
                } || {
                  af="--empty"
                }
                Stars copy -v -rel -r '4' \${af} -o ./ \${reference[0]}
                res=$?
              }
              rm -fr stagein.sh
              exit \${res}

baseCommand: ['/bin/bash', 'stagein.sh']

inputs:
  ADES_STAGEIN_AWS_SERVICEURL:
    type: string?
  ADES_STAGEIN_AWS_REGION:
    type: string?
  ADES_STAGEIN_AWS_ACCESS_KEY_ID:
    type: string?
  ADES_STAGEIN_AWS_SECRET_ACCESS_KEY:
    type: string?
outputs: {}
