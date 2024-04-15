import logging
from .log_handlers import setup_file_handler, setup_console_handler

# Define VERBOSE log level
VERBOSE = 15
logging.addLevelName(VERBOSE, "VERBOSE")

# Define VERBOSE log level function
def verbose(self, message, *args, **kws):
    if self.isEnabledFor(VERBOSE):
        self._log(VERBOSE, message, args, **kws)

logging.Logger.verbose = verbose

def setup_logger(name='CosmologyPipeline', level=VERBOSE):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Add handlers
    logger.addHandler(setup_file_handler(level))
    logger.addHandler(setup_console_handler())

    # Prevent duplicate messages
    logger.propagate = False

    return logger