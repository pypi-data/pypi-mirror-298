import re
from typing import Union, Set, Tuple, List, Dict


class MatchError(Exception):
    pass


def match(string: str,
          patterns: Union[str, Tuple[str, ...], Set[str], List[str]],
          flags: int = 0) -> Union[None, Dict[str, str], Tuple[str, ...]]:
    if not patterns:
        return

    if isinstance(patterns, str):
        patterns = [patterns]

    if not ((isinstance(patterns, tuple) or isinstance(patterns, set) or isinstance(patterns, list)) and
            all(map(lambda x: isinstance(x, str), patterns))):
        raise MatchError(f'patterns：`{patterns}` 赋值错误，其值只能是字符串、字符串元组、字符串集合和字符串列表中的一个！')

    compilers = [re.compile(pattern, flags) for pattern in patterns]
    for compiler in compilers:
        m = compiler.match(string)
        if m is None:
            continue
        groupdict = m.groupdict()  # noqa
        if groupdict:
            return groupdict
        groups = m.groups()
        if groups:
            return groups
        return

    raise MatchError(f'string：`{string}` 没有匹配 patterns：`{patterns}`！')
