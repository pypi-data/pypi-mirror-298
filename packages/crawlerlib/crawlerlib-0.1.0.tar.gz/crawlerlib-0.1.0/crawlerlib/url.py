from typing import Optional, List, Any
from furl import furl


def get_path_segments(url: str) -> List[str]:
    """
    >>> get_path_segments('https://www.baidu.com/s?wd=crawlerlib')
    ['s']

    :param url:
    :return:
    """
    return furl(url).path.segments


def get_query_param_value(url: str, key: str, default: Optional[Any] = None) -> str:
    """
    >>> get_query_param_value('https://www.baidu.com/s?wd=crawlerlib', 'wd')
    'crawlerlib'

    :param url:
    :param key:
    :param default:
    :return:
    """
    value = furl(url).query.params.get(key, default=default)
    return value
