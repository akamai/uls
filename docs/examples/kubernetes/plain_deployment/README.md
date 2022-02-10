# Kubernetes deployment

This document describes the deployment of ULS via a k8s deployment file.
This is just an example file to get you started.

## Steps
- [Create an Akamai namepsace](#create-an-akamai-namepsace)
- [Upload Akamai EDGERC FILE](#upload-akamai-edgerc-file)
- [Apply the deployment file](#apply-the-deployment-file)


### Create an Akamai namepsace
It is strongly recommended to create a dedicated namespace and **not use the "default"** namespace.
Replace `<your-namespace>` with your values then run the following command:
```text
kubectl create namespace <your-namespace>
```
_Example:_
```text
kubectl create namespace akamai-uls
```  


### Upload AKAMAI .edgerc file
Please replace `<your-namespace>` and `<your-edgerc-file>` with your values then run the following command
```text
kubectl create secret generic akamai-edgerc -n <your-namespace> --from-file=edgerc=<your-edgerc-file>
```

_Example:_
```text
kubectl create secret generic akamai-edgerc -n akamai-uls --from-file=edgerc=/home/username/.edgerc
```


### Apply the deployment file
Please replace `<your-namespace>` with your value then run the following command
```text
kubectl apply -n <your-namespace> -f uls-deployment.yml
```

_Example:_
```text
kubectl apply -n akamai-uls -f uls-deployment.yml
```