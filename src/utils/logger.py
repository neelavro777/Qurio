import logging
import sys

import os

def setup_logger(name: str = "qurio") -> logging.Logger:
    """Configures and returns a logger with console and file output."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # 1. Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # 2. File Handler (Root / logs / app.log)
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        file_handler = logging.FileHandler(os.path.join(log_dir, "app.log"))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger

# Create a default logger instance
logger = setup_logger()
