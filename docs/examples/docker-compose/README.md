# Docker-Compose Configurations
Within this directory, we provide some `docker compose` examples including example files.

The docker-compose.yml controls the docker - relevant attributes like mounting the `.edgerc` file into the container.
The `.env` files control the ULS via dedicated [ENVIRONMENTAL VARIABLES](../../ARGUMENTS_ENV_VARS.md).

The [simple](simple/README.md) directory provides a simple example running ULS via `docker compose`  
The [complex](complex/README.md) directory provides a more "real world" example combining multiple feeds and different outputs.  
The [example](examples/README.md) directory provides different configuration snippets.
The [etp-multi-tenant](etp-tenants/README.md) directory shows how logs from different ETP tenants can be collected.
