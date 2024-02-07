#!/usr/bin/env python3


# MCAS
    ## Global
mcas_name_long = "Microsoft Cloud Applican Security"
mcas_name_short = "MCAS"

    ## Requirements
mcas_required_input = ['ETP']
mcas_required_feed = ['PROXY', 'DNS']
mcas_required_cliformat = ['JSON']

    ## MCAS INPUT LOG FORMAT
mcas_input_format = "detection_time={0} client_ip={1} destination_ip={2} domain={3} user_name={4} bytes_uploaded={5} bytes_downloaded={6} bytes_total={7} action={8}"


# JMESPATH
    ## Global
jmespath_name_long = "JMESPath https://jmespath.org/"
jmespath_name_short = "JMESPath"

    ## Requirements
jmespath_required_cliformat = ['JSON']