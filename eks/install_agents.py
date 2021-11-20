import pulumi,yaml,os,json,glob
import pulumi_kubernetes as kubernetes
from pulumi_kubernetes import ConfigFile
#from baseinstall.crds import setup
#import baseinstall.crds.pulumi_crds as pulumi_crds
from pulumi import Config

#def install_manifests():
#    config = Config()

#    olm_crd = kubernetes.yaml.ConfigFile("olm_crd", file="./baseinstall/crds/olm_crd.yaml")

 #   olm_crd_install = pulumi_crds.meta_v1.ObjectMetaArgs()


