FROM            python:3.13.3-slim-bookworm
LABEL           MAINTAINER="Mike Schiessl - mike.schiessl@akamai.com"
LABEL	        APP_LONG="Akamai Unified Log Streamer"
LABEL           APP_SHORT="ULS"
LABEL           VENDOR="Akamai Technologies Inc"


# CONFIGURATION ARGS
ARG             HOMEDIR="/opt/akamai-uls"
ARG             ULS_DIR="$HOMEDIR/uls"
ARG             EXT_DIR="$ULS_DIR/ext"

ARG             ETP_CLI_VERSION="0.4.9"
ARG             EAA_CLI_VERSION="0.6.11"
ARG             MFA_CLI_VERSION="0.1.1"
ARG             GC_CLI_VERSION="v0.0.7"
ARG             LINODE_CLI_VERSION="v0.0.6"
ARG             ACC_CLI_VERSION="v0.0.1-alpha"

# ENV VARS
ENV             ULS_DIR=$ULS_DIR
ENV             EXT_DIR=$EXT_DIR
ENV             HOMEDIR=$HOMEDIR
ENV             CONTAINERIZED=TRUE

# PREPARE ENVIRONMENT
    # hadolint ignore=DL3008
RUN	            apt-get update && \
	            apt-get --no-install-recommends -y install \
		        ca-certificates \
		        git \
		        curl \
                telnet \
                gcc \
                libssl-dev \
                libffi-dev \
                acl && \
		        rm -rf /var/lib/apt/lists/



# USER & GROUP
RUN 	        groupadd akamai && \
                useradd -g akamai -s /bin/bash -m -d ${HOMEDIR} akamai

# Applying the root group to the akamai-uls directory to match openshift security requirements
#RUN             setfacl -m g:root:rx ${HOMEDIR} && \
#                setfacl -dm g:root:rx ${HOMEDIR}

# Installing now as root and switching later to the akamai user

WORKDIR         ${HOMEDIR}
RUN             mkdir -p ${ULS_DIR} && \
                mkdir -p ${ULS_DIR}/var && chmod 777 ${ULS_DIR}/var


# Install ULS
COPY            bin/ ${ULS_DIR}/bin
WORKDIR         ${ULS_DIR}
RUN             pip3 install --no-cache-dir -r ${ULS_DIR}/bin/requirements.txt


# Install external CLI'S
## ETP CLI
ENV             ETP_CLI_VERSION=$ETP_CLI_VERSION
RUN             git clone --depth 1 -b "${ETP_CLI_VERSION}" --single-branch https://github.com/akamai/cli-etp.git ${EXT_DIR}/cli-etp && \
                pip3 install --no-cache-dir -r ${EXT_DIR}/cli-etp/requirements.txt

## EAA CLI
ENV             EAA-CLI_VERSION=$EAA_CLI_VERSION
RUN             git clone --depth 1 -b "${EAA_CLI_VERSION}" --single-branch https://github.com/akamai/cli-eaa.git ${EXT_DIR}/cli-eaa && \
                pip3 install --no-cache-dir -r ${EXT_DIR}/cli-eaa/requirements.txt


## MFA CLI
ENV             MFA-CLI_VERSION=$MFA_CLI_VERSION
RUN             git clone --depth 1 -b "${MFA_CLI_VERSION}" --single-branch https://github.com/akamai/cli-mfa.git ${EXT_DIR}/cli-mfa && \
                pip3 install --no-cache-dir -r ${EXT_DIR}/cli-mfa/requirements.txt

## GuardiCore CLI
ENV             GC_CLI_VERSION=$GC_CLI_VERSION
RUN             git clone --depth 1 -b "${GC_CLI_VERSION}" --single-branch https://github.com/MikeSchiessl/gc-logs.git ${EXT_DIR}/cli-gc && \
                pip3 install --no-cache-dir -r ${EXT_DIR}/cli-gc/bin/requirements.txt

## LINODE CLI
ENV             LINODE_CLI_VERSION=$LINODE_CLI_VERSION
RUN             git clone --depth 1 -b "${LINODE_CLI_VERSION}" --single-branch https://github.com/MikeSchiessl/ln-logs.git ${EXT_DIR}/cli-linode && \
                pip3 install --no-cache-dir -r ${EXT_DIR}/cli-linode/bin/requirements.txt

## ACC CLI
ENV             ACC_CLI_VERSION=$ACC_CLI_VERSION
RUN             git clone --depth 1 -b "${ACC_CLI_VERSION}" --single-branch https://github.com/MikeSchiessl/acc-logs.git ${EXT_DIR}/acc-logs && \
                pip3 install --no-cache-dir -r ${EXT_DIR}/acc-logs/bin/requirements.txt


# Preparing user - switch
#RUN             chown -R akamai:root ${HOMEDIR}
USER            akamai


# ENTRYPOINTS / CMD
VOLUME          ["${ULS_DIR}/var"]
ENTRYPOINT      ["/usr/local/bin/python3","-u","bin/uls.py"]
# EOF
