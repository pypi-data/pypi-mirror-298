DEFAULT_LOGGER = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {  # correlation ID filter must be added here to make the %(correlation_id)s formatter work
        'correlation_id': {'()': 'finalsa.common.lambdas.logger.filter.CorrelationIdFilter'},
    },
    'formatters': {
        'console': {
            'class': 'app.logger.CustomJsonFormatter',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['correlation_id'],
            'formatter': 'console',
        },
    },
    # Loggers can be specified to set the log-level to log, and which handlers to use
    'loggers': {
        # project logger
        'root': {'handlers': ['console'], 'level': 'INFO', 'propagate': True},
    },
}
