import logging

def init(loglevel='WARNING', loggername=None):
    global log
    log = logging.getLogger(loggername)
    logging.basicConfig(format='%(asctime)s %(name)s %(levelname).1s %(message)s')
    log.setLevel(loglevel)
    log.debug("Logging initialized")
    return log

# EOF
