from collections.abc import Iterable
import re
from typing import Any, cast

from structured_templates.context import Context
from structured_templates.types import Value


class TemplateEngine:
    """
    Template engine for structured templates.
    """

    def __init__(self, globals_: dict[str, Any] | None = None):
        self.globals = globals_ or {}

    def evaluate(self, value: Value | Context[Value], recursive: bool = True) -> Value:
        """
        Evaluate the given value.
        """

        if not isinstance(value, Context):
            value = Context(None, None, value)

        match value.data:
            case dict():
                return self.evaluate_dict(cast(Context[dict[str, Value]], value), recursive)
            case list():
                return self.evaluate_list(cast(Context[list[Value]], value), recursive)
            case str():
                return self.evaluate_string(cast(Context[str], value))
            case _:
                return value.data

    def evaluate_dict(self, ctx: Context[dict[str, Value]], recursive: bool) -> dict[str, Value] | list[Value]:
        """
        Evaluate the given dictionary.
        """

        result: dict[str, Value] = {}
        for key, value in ctx.data.items():
            subctx = Context(ctx, key, value)

            if key.startswith("if(") and key.endswith(")"):
                if self.evaluate_expression(Context(ctx, key, key[3:-1])):
                    # We require a dict, but if it's a string we want to evaluate it first.
                    if isinstance(value, str):
                        value = self.evaluate_string(Context(ctx, key, value))
                    if not isinstance(value, dict):
                        raise subctx.error("The value of an if block must be a dictionary.")

                    if recursive:
                        value = self.evaluate_dict(Context(ctx, key, value), recursive)

                    if not isinstance(value, dict):
                        raise subctx.error(f"if() must evaluate to a mapping, got {type(value).__name__}")
                    result.update(value)

            elif key.startswith("for(") and key.endswith(")"):
                if not isinstance(value, dict):
                    raise subctx.error("The value of a for block must be a dictionary.")

                expr = key[4:-1]  # TODO: Better parsing of the for block syntax
                if " in " not in expr:
                    raise subctx.error(f"Invalid for block expression (missing 'in'): {expr}")

                var, iterable = expr.split(" in ")
                if not var.isidentifier():
                    raise subctx.error(f"Invalid for block variable (not an identifier): {var}")

                it = self.evaluate_expression(Context(ctx, key, iterable))
                if not isinstance(it, Iterable):
                    raise subctx.error(f"The iterable of a for block must be iterable, got {type(it).__name__}.")

                for idx, item in enumerate(it):
                    if not recursive:
                        result[f"with({var}={item!r})"] = value
                    else:
                        new_value = self.evaluate_dict(Context(subctx, str(idx), value, {var: item}), recursive)
                        if not isinstance(new_value, dict):
                            raise subctx.error(f"for() must evaluate to a mapping, got {type(new_value).__name__}")
                        result.update(new_value)

            elif key.startswith("with(") and key.endswith(")"):
                if not isinstance(value, dict):
                    raise subctx.error("The value of a with block must be a dictionary.")

                # TODO: Support multiple assignments
                expr = key[5:-1]
                if "=" not in expr:
                    raise subctx.error(f"Invalid with block expression (missing '='): {expr}")

                var, val = expr.split("=")
                if not var.isidentifier():
                    raise subctx.error(f"Invalid with block variable (not an identifier): {var}")

                val = self.evaluate_expression(Context(ctx, key, val))
                new_value = self.evaluate_dict(Context(subctx, var, value, {var: val}), recursive)
                if not isinstance(new_value, dict):
                    raise subctx.error(f"with() must evaluate to a mapping, got {type(new_value).__name__}")
                result.update(new_value)

            elif key == "merge()":
                if not isinstance(value, list):
                    value = [value]

                for item in value:
                    item = self.evaluate(Context(ctx, key, item), recursive)
                    if not isinstance(item, dict):
                        raise subctx.error(f"Expected a dictionary, got {type(item).__name__}")
                    result.update(item)

            elif key == "concat()":
                if len(ctx.data) != 1:
                    raise subctx.error(f"concat() can only be used in a mapping with one key, got {ctx.data.keys()}")
                if not isinstance(value, list):
                    raise subctx.error(f"concat() value must be a list, got {type(value).__name__}")

                new_list: list[Any] = []
                for idx, item in enumerate(value):
                    if item is None:
                        continue
                    if not isinstance(item, list):
                        raise subctx.error(f"item {idx} to concat() must be a list, got {type(value).__name__}")
                    new_list.extend(item)

                return new_list

            else:
                key_value = self.evaluate_string(Context(ctx, key, key))
                if not isinstance(key_value, str):
                    raise subctx.error(f"Expected a string key, got {type(key_value).__name__}")
                if recursive or isinstance(value, str):
                    value = self.evaluate(Context(ctx, key, value), recursive)
                result[key_value] = value

        return result

    def evaluate_list(self, ctx: Context[list[Value]], recursive: bool) -> list[Value]:
        """
        Evaluate the given list.
        """

        return [self.evaluate(Context(ctx, idx, item), recursive) for idx, item in enumerate(ctx.data)]

    def evaluate_string(self, ctx: Context[str]) -> Value:
        """
        Evaluate the given string.
        """

        if ctx.data.startswith("${{") and ctx.data.endswith("}}"):
            return self.evaluate_expression(Context(ctx.parent, ctx.key, ctx.data[3:-2]))

        def _repl(m: re.Match[str]) -> str:
            result = self.evaluate_expression(Context(ctx.parent, ctx.key, m.group(1)))
            if not isinstance(result, int | float | str | bool | None):
                raise ctx.error(f"Expected a plain value, got {type(result).__name__}")
            return str(result) if result is not None else ""

        return re.sub(r"\$\{\{(.+?)\}\}", _repl, ctx.data)

    def evaluate_expression(self, ctx: Context[str]) -> Any:
        """
        Evaluate the given expression.
        """

        try:
            # TODO: Don't manifest full ChainMap, this is a huge performance hit.
            return eval(ctx.data, dict(ctx.full_scope(self.globals)))
        except Exception as e:
            raise ctx.error(f"Failed to evaluate the expression: {e}") from e
