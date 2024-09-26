__all__ = ["proprietary"]


def proprietary(old, /):
    kwargs = dict()
    link(old, "getter", kwargs, "fget")
    link(old, "setter", kwargs, "fset")
    link(old, "deleter", kwargs, "fdel")
    link(old, "__doc__", kwargs, "doc")
    ans = property(**kwargs)
    return ans


def link(old, name, kwargs, key):
    try:
        kwargs[key] = getattr(old, name)
    except AttributeError:
        return
