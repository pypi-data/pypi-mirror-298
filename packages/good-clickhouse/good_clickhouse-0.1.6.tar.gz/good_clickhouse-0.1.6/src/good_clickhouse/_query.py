from __future__ import annotations
import typing
from dataclasses import dataclass
import inspect
import re

from jinja2 import Environment, StrictUndefined, BaseLoader


@dataclass
class Query:
    instance_registry: typing.ClassVar[dict[str, Query]] = {}

    @classmethod
    def register(cls, name: str, query: Query):
        cls.instance_registry[name] = query

    @classmethod
    def patch_env(cls, env: Environment):
        for name, query in cls.instance_registry.items():
            env.globals[f"query_{name}"] = query

    template: str
    signature: inspect.Signature

    def __post_init__(self):
        self.parameters: list[str] = list(self.signature.parameters.keys())

    def __call__(self, *args, **kwargs) -> str:
        """Render and return the template.

        Returns
        -------
        The rendered template as a Python ``str``.

        """
        bound_arguments = self.signature.bind(*args, **kwargs)
        bound_arguments.apply_defaults()
        return render(self.template, **bound_arguments.arguments)

    def __str__(self):
        return self.template


def query(fn: typing.Callable) -> Query:
    """Decorate a function that contains a query template.

    >>> @query
    >>> def count_table(table_name: str):
    ...    '''select count(*) from {{ table_name }};'''
    ...


    Returns
    -------
    A `Query` callable class which will render the template when called.

    """

    signature = inspect.signature(fn)

    # The docstring contains the template that will be rendered to be used
    # as a prompt to the language model.
    docstring = fn.__doc__
    if docstring is None:
        raise TypeError("Could not find a template in the function's docstring.")

    template = typing.cast(str, docstring)

    q = Query(template, signature)
    Query.register(fn.__name__, q)
    return q


def render(template: str, **values: dict[str, typing.Any] | None) -> str:
    # Dedent, and remove extra linebreak
    cleaned_template = inspect.cleandoc(template)

    # Add linebreak if there were any extra linebreaks that
    # `cleandoc` would have removed
    ends_with_linebreak = template.replace(" ", "").endswith("\n\n")
    if ends_with_linebreak:
        cleaned_template += "\n"

    # Remove extra whitespaces, except those that immediately follow a newline symbol.
    # This is necessary to avoid introducing whitespaces after backslash `\` characters
    # used to continue to the next line without linebreak.
    cleaned_template = re.sub(r"(?![\r\n])(\b\s+)", " ", cleaned_template)

    env = Environment(
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        undefined=StrictUndefined,
        loader=BaseLoader(),
    )

    Query.patch_env(env)

    jinja_template = env.from_string(cleaned_template)

    return jinja_template.render(**values)
