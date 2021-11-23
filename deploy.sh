#!/bin/bash

export STACK_NAME=$1
export ACTION=$2
export EXTRA_OPTS=${*:3}
export PULUMI_CONFIG_PASSPHRASE='Sc2016csc!'
export AWS_PROFILE="scoadycloud"
echo "Checking config for stack: $STACK_NAME"
export config_yaml=$(find ./config -name "Pulumi.$STACK_NAME.yaml")
echo "Found config file: $config_yaml"
export STACK_TYPE=$(echo $config_yaml|rev|cut -d/ -f3|rev)
echo "Searching for common.yaml in ./config/$STACK_TYPE/"
export common_yaml=$(find ./config/$STACK_TYPE -name "common.yaml")
echo "Found common yaml file: $common_yaml"
yaml-merge $common_yaml $config_yaml |tee ./$STACK_TYPE/Pulumi.$STACK_NAME.yaml
echo "Copied to: ./$STACK_TYPE/Pulumi.$STACK_NAME.yaml"
cd $STACK_TYPE
pulumi stack select $STACK_NAME
export region=$(pulumi config get region)
export cluster_name=$(pulumi config get cluster_name)
export skip_initial_kubeconfig=$(pulumi config get skip_initial_validation)
echo "Skip initial: $skip_initial_kubeconfig"
if [ "$skip_initial_kubeconfig" == "true" ];
then
    echo "Skipping kubeconfig generation"

else
    echo "Generating kubeconfig.. region: $region, cluster: $cluster_name"
    aws eks --region $region update-kubeconfig --name $cluster_name --profile $AWS_PROFILE
    export current_context=$(kubectl config current-context)

fi
echo "Running: pulumi $ACTION $EXTRA_OPTS"
pulumi $ACTION $EXTRA_OPTS


