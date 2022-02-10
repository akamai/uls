# HELM Usage for AKAMAI ULS

This document describes the installation of the ULS [HELM CHART](https://helm.sh/)

## Steps
- [Create an Akamai namepsace](#create-an-akamai-namepsace)
- [Upload Akamai EDGERC FILE](#upload-akamai-edgerc-file)
- 


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
Replace `<your-namespace>` and `<your-edgerc-file>` with your values then run the following command:
```text
kubectl create secret generic akamai-edgerc -n <your-namespace> --from-file=edgerc=<your-edgerc-file>
```

_Example:_
```text
kubectl create secret generic akamai-edgerc -n akamai-uls --from-file=edgerc=/home/username/.edgerc
```

### Install HELM chart
Replace `<your-namespace>` and `<your-install-name>` with your values then run the following command:
```text
helm install --namespace <your-namespace> <your-install-name> akamai-uls
```
Example: 
```text
helm install --namespace akamai-uls uls-etp-threat akamai-uls 
```

In addition you can provide all of the known [ULS environment variables](../../../ARGUMENTS_ENV_VARS.md)
- via CLI flags
    ```text
    # RUN EAA with TCP output 
    helm install --namespace akamai-uls uls-etp-threat akamai-uls --set akamai_uls.environment.ULS_INPUT=EAA --set akamai_uls.environment.ULS_FEED=ACCESS --set akamai_uls.environment.ULS_OUTPUT=TCP --set akamai_uls.environment.ULS_HOST=my_tcp_host.my.tld --set akamai_uls.environment.ULS_PORT=666
    ```

- via value file  
File Example `my_values.yml`:
```text
akamai_uls:
    environment:
      ULS_INPUT: "EAA"
      ULS_FEED: "CONHEALTH"
      ULS_LOGLEVEL: "DEBUG"
      ULS_OUTPUT: "HTTP"
      ULS_HTTP_URL: "https://my_cool_http_input.siem.tld"
      ULS_HTTP_AUTH_HEADER: '{"Authorization": "XOXOXOXOXOXOXOXOX"}'
```

```text
helm install --namespace akamai-uls -f my_values.yml uls-etp-threat akamai-uls 
```