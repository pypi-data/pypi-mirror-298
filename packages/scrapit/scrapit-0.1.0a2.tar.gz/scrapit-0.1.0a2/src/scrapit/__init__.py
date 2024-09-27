from datetime import date, datetime, tzinfo
from functools import cached_property
from itertools import chain
import re
from typing import Any, Callable, Self

from lxml.etree import ElementTree
import lxml.html
from pytz import timezone


class Document:
    def __init__(
        self,
        data: Any | list[Any],
        base_url: str | None = None,
        ns: dict[str, str] | None = None,
    ):
        self.data = data
        self.base_url = base_url
        self.ns = ns

    @classmethod
    def from_html(
        cls,
        content: str,
        base_url: str | None = None,
        ns: dict[str, str] | None = None,
    ) -> Self:
        data = lxml.html.fromstring(content, base_url=base_url)
        return cls(data, base_url=base_url, ns=ns)

    @cached_property
    def is_empty(self) -> bool:
        return self.data is None or self.data == []

    @cached_property
    def is_scalar(self) -> bool:
        return not isinstance(self.data, list)

    @cached_property
    def depth(self) -> int:
        def depth_recursive(values):
            if not isinstance(values, list):
                return 0
            else:
                return max(depth_recursive(v) for v in values) + 1
        return depth_recursive(self.data)

    @cached_property
    def shape(self) -> int | list[int | list, ...]:
        def shape_recursive(values: list):
            if values is None:
                return 0
            elif not isinstance(values, list):
                return 1
            elif all(not isinstance(v, list) for v in values):
                return [len(values)]
            else:
                return list(shape_recursive(v) for v in values)
        return shape_recursive(self.data)

    @property
    def value(self) -> ElementTree:
        if self.is_scalar:
            return self.data
        else:
            raise ValueError('Document data is not scalar')

    @property
    def values(self) -> list[ElementTree]:
        if self.is_scalar:
            return [self.data]
        else:
            return self.data

    def __len__(self) -> int:
        if self.is_scalar:
            raise ValueError('Scalar document does not support len()')
        return len(self.data)

    def __iter__(self) -> Self:
        if self.is_scalar:
            raise ValueError('Scalar document does not support iteration')
        for item in self.data:
            yield Document(item)

    # non-terminal selectors

    def css(self, expr: str, merge: bool = True) -> Self:
        if self.is_empty:
            return self
        data = _apply(self.data, lambda et: et.cssselect(expr), merge=merge)
        return Document(data)

    def xpath(self, expr: str, merge: bool = True) -> Self:
        if self.is_empty:
            return self
        data = _apply(self.data, lambda et: et.xpath(expr, namespaces=self.ns), merge=merge)
        return Document(data)

    def __getitem__(self, item) -> Self:
        if self.is_scalar:
            raise ValueError('Scalar document does not support item access')
        try:
            return Document(self.data[item])
        except IndexError:
            return Document(None)

    def merge(self) -> Self:
        if self.is_scalar:
            return self
        return Document(_merge_all(self.data))

    def select(self, selector: Callable, *args, **kwargs) -> Self:
        if self.is_empty:
            return self
        result = selector(self, *args, **kwargs)
        if isinstance(result, list):
            return Document([doc.data for doc in result])
        else:
            return result

    # terminal selectors

    def attrib(self, name: str) -> Any | list:
        if self.is_empty:
            return self
        return _apply(self.data, lambda et: et.attrib[name])

    def date(self, fmt: str, merge: bool | str = False) -> date | list | None:
        if self.is_empty and self.is_scalar:
            return None
        def parse_date(v: str) -> date | None:
            try:
                return datetime.strptime(v, fmt).date()
            except:
                return None
        return _apply(data=self.text(merge=merge), func=parse_date, merge=False)

    def datetime(
        self,
        fmt: str,
        merge: bool | str = False,
        tz: str | tzinfo | None = None,
    ) -> datetime | list | None:
        if self.is_empty and self.is_scalar:
            return None
        def parse_datetime(v: str) -> datetime | None:
            try:
                naive = datetime.strptime(v, fmt)
                aware = naive.replace(tzinfo=timezone(tz) if isinstance(tz, str) else tz)
                return aware
            except:
                return None
        return _apply(data=self.text(merge=merge), func=parse_datetime, merge=False)

    def float(self, sep='.', merge: bool | str = False) -> float | list | None:
        if self.is_empty and self.is_scalar:
            return None
        nonfloat = re.compile(rf'[^-0-9{sep}e]+')
        seps = re.compile(rf'[{sep}]+')
        def parse_float(v: str) -> float | None:
            try:
                return float(seps.sub('.', nonfloat.sub('', v)))
            except:
                return None
        return _apply(data=self.text(merge=merge), func=parse_float, merge=False)

    def int(self, merge: bool | str = False) -> int | list | None:
        if self.is_empty and self.is_scalar:
            return None
        nonint = re.compile(rf'[^-0-9]+')
        def parse_int(v: str) -> float | None:
            try:
                return int(nonint.sub('', v))
            except:
                return None
        return _apply(data=self.text(merge=merge), func=parse_int, merge=False)

    def text(self, strip: bool = True, merge: bool | str = False) -> str | list | None:
        if not (merge is False or isinstance(merge, str)):
            raise ValueError('Merge must be False or string')
        if self.is_empty and self.is_scalar:
            return None
        to_text = lambda et: (et.text_content().strip() if strip else et.text_content())
        data = _apply(self.data, to_text, merge=False)
        if merge is False:
            return data
        else:
            return merge.join(_merge_all(data))


# helpers

def _apply(data, func: Callable, merge: bool = False) -> Any:
    def apply_recursive(values: list):
        if values is None:
            return None
        elif not isinstance(values, list):
            return func(values)
        elif all(not isinstance(v, list) for v in values):
            if merge:
                return list(chain.from_iterable(func(v) for v in values))
            else:
                return [func(v) for v in values]
        else:
            return [apply_recursive(v) for v in values]
    return apply_recursive(data)


def _merge_all(data) -> list[Any] | Any:
    def merge_recursive(values):
        if not isinstance(values, list):
            return values
        else:
            items = []
            for item in [merge_recursive(v) for v in values]:
                if isinstance(item, list):
                    items.extend(item)
                else:
                    items.append(item)
            return items
    return merge_recursive(data)
