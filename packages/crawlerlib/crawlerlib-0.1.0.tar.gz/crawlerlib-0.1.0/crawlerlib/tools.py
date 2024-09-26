from typing import Union


def format_price(price: Union[int, float, str], places: int = 2) -> str:
    """
    >>> format_price(3.1)
    '3.10'

    :param price:
    :param places:
    :return:
    """
    integer_str, decimal_str = str(float(price)).split('.')
    decimal_str = (decimal_str + '0' * (places - len(decimal_str)))[:places]
    price_str = '.'.join([integer_str, decimal_str])
    return price_str
