#!/bin/bash


export stacks=($(find ./config -name "Pulumi.*.yaml"))

echo "There are: ${#stacks[@]} stacks to preview updates for. This might take a while..."

for stack in ${stacks[@]}
do
    export stack_name=$(echo $stack|rev|cut -d/ -f2|rev)
    echo "Stack Name: $stack_name, Config location: $stack"
done
