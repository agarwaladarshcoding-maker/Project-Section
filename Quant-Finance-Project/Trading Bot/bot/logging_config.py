import logging
import sys
def setup_logger(log_file="bot_order_file.log"):
    # Configures a centralized logger that outputs to both a file and the console
    logger = logging.getLogger("BinanceBotLogger")
    #Setting the level of log Info
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        #  Attach Handlers to the Logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger
    



