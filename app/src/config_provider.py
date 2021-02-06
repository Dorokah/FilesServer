import os


def get_algorithm_name():
    return os.environ.get('APP_NAME', 'APP')


def get_algorithm_version():
    return os.environ.get('VERSION', 'Beta')


def get_algorithm_description():
    return os.environ.get('APP_DESCRIPTION',
                          'Algorithm by XXXX will detected XXXX in a given image.')


def get_port():
    return os.environ.get('PORT', '8000')


def get_workers():
    return int(os.environ.get('WORKERS', '1'))


def get_timeout():
    return int(os.environ.get('TIMEOUT', '5000'))


def get_log_level():
    return os.environ.get('LOG_LEVEL', 'DEBUG')


def get_config():
    return {
        'appName': get_algorithm_name(),
        'appVersion': get_algorithm_version(),
        'appDescription': get_algorithm_description(),
        'workers': get_workers(),
        'logLevel': get_log_level(),
        'timeout': get_timeout(),
        'port': get_port(),
    }
