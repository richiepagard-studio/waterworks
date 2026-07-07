LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'standard': {
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
        }
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'filters': [],
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'filters': []
        }
    },

    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True
        },
        'django.request': {
            'handlers': 'file',
            'level': 'ERROR',
            'propagate': False
        }
    }
}