import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# Create handlers
console_handler = logging.StreamHandler()
# Create formatters and add it to handlers
format_log = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(format_log)
# Add handlers to the helpers
log.addHandler(console_handler)