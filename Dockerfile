FROM            python:3.10.4-slim-bullseye
LABEL 	        MAINTAINER="Mike Schiessl - mike.schiessl@akamai.com"
LABEL	        APP_LONG="Akamai Universal Log Streamer"
LABEL           APP_SHORT="ULS"
LABEL           VENDOR="Akamai Technologies"


# CONFIGURATION ARGS
ARG             HOMEDIR="/opt/akamai-uls"
ARG             ULS_DIR="$HOMEDIR/uls"
ARG             EXT_DIR="$ULS_DIR/ext"

ARG             ETP_CLI_VERSION="0.3.8"
ARG             EAA_CLI_VERSION="0.5.0"
ARG             MFA_CLI_VERSION="0.0.9"

# ENV VARS
ENV             ULS_DIR=$ULS_DIR
ENV             EXT_DIR=$EXT_DIR
ENV             HOMEDIR=$HOMEDIR


# PREPARE ENVIRONMENT
# ENV PREP
RUN	            apt-get update && \
	            apt-get --no-install-recommends -y install \
		        ca-certificates \
		        git \
		        curl \
                telnet \
                gcc libssl-dev libffi-dev  && \
		        rm -rf /var/lib/apt/lists/

# USER & GROUP
RUN 	        groupadd akamai && \
                useradd -g akamai -s /bin/bash -m -d ${HOMEDIR} akamai

USER            akamai
WORKDIR         ${HOMEDIR}
RUN             mkdir -p ${ULS_DIR}


# Install ULS
COPY            bin/ ${ULS_DIR}/bin
COPY            var/ ${ULS_DIR}/var
WORKDIR         ${ULS_DIR}
RUN             pip3 install -r ${ULS_DIR}/bin/requirements.txt

# Install external CLI'S
## ETP CLI
ENV             ETP_CLI_VERSION=$ETP_CLI_VERSION
RUN             git clone --depth 1 -b "${ETP_CLI_VERSION}" --single-branch https://github.com/akamai/cli-etp.git ${EXT_DIR}/cli-etp && \
                pip3 install -r ${EXT_DIR}/cli-etp/requirements.txt

## EAA CLI
ENV             EAA-CLI_VERSION=$EAA_CLI_VERSION
RUN             git clone --depth 1 -b "${EAA_CLI_VERSION}" --single-branch https://github.com/akamai/cli-eaa.git ${EXT_DIR}/cli-eaa && \
                pip3 install -r ${EXT_DIR}/cli-eaa/requirements.txt


## MFA CLI
ENV             MFA-CLI_VERSION=$MFA_CLI_VERSION
RUN             git clone --depth 1 -b "${MFA_CLI_VERSION}" --single-branch https://github.com/akamai/cli-mfa.git ${EXT_DIR}/cli-mfa && \
                pip3 install -r ${EXT_DIR}/cli-mfa/requirements.txt

# ENTRYPOINTS / CMD
VOLUME          ["${ULS_DIR}/var"]
ENTRYPOINT      ["/usr/local/bin/python3","-u","bin/uls.py"]
#CMD             ["--help"]
# EOF
