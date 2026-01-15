import logging

class StaticFileFilter(logging.Filter):
    def filter(self, record):
        # Filter out log records containing /static/
        return '/static/' not in record.getMessage()
