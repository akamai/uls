# ULS High Availability
This document describes high availability options for the ULS software.  
ULS itself does not bring HA capabilities out of the box, but it was built to support different HA techniques.  

## Docker
To use high availability alongside with the provided ULS docker container, a HA orchestration layer like [SWARM](https://docs.docker.com/engine/swarm/), [KUBERNETES](https://kubernetes.io/) or [others](https://devopscube.com/docker-container-clustering-tools/) is required.  
It is highly recommended, to enable the ULS auto-resume feature and store the according "resume - data" on a persistent volume which is available accross different compute nodes (e.g. PVC, NFS, ...).  
This setup allows the ULS container(s) to maintain HA across multiple compute nodes.

## Daemon
Whenever container usage isn't an option, high availability can be achieved by using OS-based high availability systems like [pacemaker](https://clusterlabs.org/) / [corosync](https://de.wikipedia.org/wiki/Corosync_Cluster_Engine) or [heartbeat](http://www.linux-ha.org/wiki/Heartbeat).  
To avoid duplicate events in the SIEM, it is highly recommended to enable the ULS auto-resume feature and store the according "resume - data" on a persistent volume that is available across the designated n odes (e.g. DRBD, NFS, ...).  
