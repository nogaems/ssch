import requests
import logging as log


class SosuchRequestError(Exception):
    pass


class SosuchParserError(Exception):
    pass


def get_request(url, proxies):
    try:
        response = requests.get(url, proxies=proxies)
    except Exception as e:
        log.error('Internet connection issue: {}'.format(e))
        raise SosuchRequestError
    if response.status_code != 200:
        log.error('Error: {} {}'.format(response.status_code,
                                        response.reason))
        raise SosuchRequestError
    return response


def safe(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (NameError, KeyError) as e:
            log.error(e)
    return wrapper
