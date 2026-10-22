import logging

logger = logging.getLogger("AI_QA_Framework")

logger.setLevel(logging.INFO)

# StreamHandler sends log messages to the console/terminal.
stream_handler = logging.StreamHandler()

# FileHandler saves log messages into a file.
file_handler = logging.FileHandler("logs/test.log")

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

# Apply the same format to both handlers.
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Connect both handlers to our logger.
logger.addHandler(stream_handler)
logger.addHandler(file_handler)