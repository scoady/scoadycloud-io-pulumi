        JSON="{\"include\":["
        export top_level_dirs=($(find . -type d -name "config"))
        export stack_names=()

        for dir in "${top_level_dirs[@]}"
        do
          export hits=($(find $dir -name "Pulumi.*.yaml"))
          for hit in ${hits[@]}
          do
            export stack=$(echo $hit|rev|cut -d/ -f2|rev)
            export project=$(echo $hit|rev|cut -d/ -f4|rev)
            
            JSON+="""{\"stack\" :\"$stack\", \"project\" : \"$project\"},"""
          done
        done
        echo "${stack_names[@]}"

        # Remove last "," and add closing brackets
        if [[ $JSON == *, ]]; then
          JSON="${JSON%?}"
        fi
        JSON="$JSON]}"
        echo $JSON
