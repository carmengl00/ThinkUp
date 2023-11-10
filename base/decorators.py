from functools import wraps
from strawberry.types import Info
import inspect

from base.utils import get_context

def with_info(target):
    def signature_add_fn(self, info: Info, *args, **kwargs):
        # Only called when no info should be passed, no need to check
        return target(self, *args, **kwargs)

    # Create a fake target function with info argument
    target_inspection = inspect.signature(target)
    if "info" not in target_inspection.parameters.keys():
        signature_add_fn.__signature__ = inspect.Signature(
            [
                *target_inspection.parameters.values(),
                inspect.Parameter("info", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=Info),
            ],
            return_annotation=target_inspection.return_annotation,
        )
        # Copy annotations as well
        signature_add_fn.__annotations__ = target.__annotations__
        return signature_add_fn
    return target

def context(func):
    def wrapper(*args, **kwargs):
        info = kwargs.get("info")
        ctx = get_context(info)
        return func(ctx, *args, **kwargs)

    return wrapper

def user_passes_test(test_func):
    def decorator(f):
        # get_result is used by strawberry-graphql-django model mutations
        get_result = getattr(f, "get_result", None)

        if get_result is not None and callable(get_result):
            f.get_result = decorator(f.get_result)
            return f

        f_with_info = with_info(f)

        @wraps(f_with_info)
        @context
        def wrapper(context, *args, **kwargs):
            if context and test_func(context.user):
                return dispose_extra_kwargs(f_with_info)(*args, **kwargs)
            raise PermissionError("You are not allowed to perform this action")

        return wrapper

    return decorator

login_required = user_passes_test(lambda u: u.is_authenticated)

def dispose_extra_kwargs(fn):
    @wraps(fn)
    def wrapper(src, *args_, **kwargs_):
        root = {}
        if src:
            args_ = args_[1:]
        present = inspect.signature(fn).parameters.keys()
        for key, val in kwargs_.items():
            if key not in present:
                root[key] = val
        passed_kwargs = {k: v for k, v in kwargs_.items() if k in present}
        if src:
            return fn(src, root, *args_, **passed_kwargs)
        if not root:
            return fn(src, *args_, **passed_kwargs)
        return fn(root, *args_, **passed_kwargs)

    return wrapper
