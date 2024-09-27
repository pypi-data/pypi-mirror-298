DEFAULT_LOGGER = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
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
    'loggers': {
        'root': {'handlers': ['console'], 'level': 'INFO', 'propagate': True},
    },
}
