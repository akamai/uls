FROM            python:3.9.6-slim-buster
LABEL 	        maintainer="Mike Schiessl - mike.schiessl@akamai.com"
LABEL	        APP="Akamai Universal Log Streamer"

# CONFIGURATION ARGS
ARG             HOMEDIR="/opt/akamai-uls"
ARG             ULS_DIR="$HOMEDIR/uls"
ARG             EXT_DIR="$ULS_DIR/ext"

ARG             ETP_CLI_VERSION="0.3.5"
ARG             EAA_CLI_VERSION="0.4.0"
ARG             MFA_CLI_VERSION="0.0.5"

# ENV VARS
ENV             ULS_DIR=$ULS_DIR
ENV             EXT_DIR=$EXT_DIR
ENV             HOMEDIR=$HOMEDIR


# PREPARE ENVIRONMENT
# ENV PREP
RUN	            apt-get update && \
	            apt-get --no-install-recommends -y install \
		        curl \
		        ca-certificates \
		        git && \
		        rm -rf /var/lib/apt/lists/

# USER & GROUP
RUN 	        groupadd akamai && \
                useradd -g akamai -s /bin/bash -m -d ${HOMEDIR} akamai

USER            akamai
WORKDIR         ${HOMEDIR}
RUN             mkdir -p ${HOMEDIR}/uls


# Install ULS
COPY            bin/ ${ULS_DIR}/bin
WORKDIR         ${ULS_DIR}

# Install external CLI'S
## ETP CLI
ENV             ETP_CLI_VERSION=$ETP_CLI_VERSION
RUN             git clone --depth 1 -b "${ETP_CLI_VERSION}" --single-branch https://github.com/akamai/cli-etp.git ${EXT_DIR}/cli-etp && \
                pip install -r ${EXT_DIR}/cli-etp/requirements.txt

## EAA CLI
ENV             EAA-CLI_VERSION=$EAA_CLI_VERSION
RUN             git clone --depth 1 -b "${EAA_CLI_VERSION}" --single-branch https://github.com/akamai/cli-eaa.git ${EXT_DIR}/cli-eaa && \
                pip install -r ${EXT_DIR}/cli-eaa/requirements.txt
## MFA CLI
ENV             MFA-CLI_VERSION=$MFA_CLI_VERSION
RUN             git clone --depth 1 -b "${MFA_CLI_VERSION}" --single-branch https://github.com/akamai/cli-mfa.git ${EXT_DIR}/cli-mfa && \
                pip install -r ${EXT_DIR}/cli-mfa/requirements.txt

# ENTRYPOINTS / CMD
#CMD             /usr/local/bin/python3 ${ULS_DIR}/bin/uls.py
ENTRYPOINT      ["/usr/local/bin/python3","bin/uls.py"]

# EOF
