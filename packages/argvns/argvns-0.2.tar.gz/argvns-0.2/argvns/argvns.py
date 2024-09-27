from argparse import Action, ArgumentParser, Namespace
from collections.abc import Callable, Sequence, Iterable
from dataclasses import dataclass, field
from typing import Generic, TypeVar, Type, Literal

T = TypeVar("T")


def argvns(cls):
    parser = ArgumentParser()

    cls.__args__ = dict()

    for key, value in vars(cls).items():
        if isinstance(value, Arg):
            cls.__args__[key] = value
            value.add_to_parser(parser)

    def init(self, args: Sequence[str] | None = None, namespace: Namespace | None = None):
        for k, v in vars(parser.parse_args(args, namespace)).items():
            arg = cls.__args__[k]

            if v is None:
                # the value isn't set in the command line
                setattr(self, k, None)
                continue

            try:
                arg.check_valid_assignment(v)
            except ValueError as e:
                raise ValueError(f"Invalid value {v!r} for key {k!r}: {e}") from e
            else:
                setattr(self, k, v)

    def repr_(self) -> str:
        clsname = cls.__name__
        args = ", ".join(f"{k}={getattr(self, k)!r}" for k in cls.__args__.keys())
        return f"{clsname}({args})"

    cls.__init__ = init
    cls.__repr__ = repr_
    return cls


@dataclass(frozen=True, kw_only=True)
class Arg(Generic[T]):
    name: str | None = None
    short: str | Sequence[str] | None = None
    long: str | Sequence[str] | None = None
    type: Callable[[str], T] = str
    choices: Iterable[T] | None = None
    nargs: int | Literal["+", "*", "?"] | None = None
    dest: str | None = None
    default: T | None = None
    const: T | None = None
    required: bool | None = None
    help: str | None = None
    action: str | Type[Action] = "store"
    validators: Iterable[tuple[Callable[[T], bool], str]] = field(default_factory=list)

    def add_to_parser(self, parser: ArgumentParser):
        """Add this argument to the given ArgumentParser."""
        name_or_flags: list[str] = []
        if self.name is not None:
            name_or_flags.append(self.name)

        if isinstance(self.short, str):
            name_or_flags.append(self.short)
        elif isinstance(self.short, Sequence):
            name_or_flags.extend(self.short)

        if isinstance(self.long, str):
            name_or_flags.append(self.long)
        elif isinstance(self.long, Sequence):
            name_or_flags.extend(self.long)

        # if required was not passed as an argument, determine if the arg should be required:
        # required if neither short nor long flags were given, not required otherwise
        required = (not self.short and not self.long) if self.required is None else self.required

        kwargs = dict(action=self.action, dest=self.dest, type=self.type, default=self.default, nargs=self.nargs,
                      choices=self.choices, const=self.const, required=required, help=self.help)

        if self.action == "store_true" or self.action == "store_false":
            kwargs.pop("type")
            kwargs.pop("const")
            kwargs.pop("nargs")
            kwargs.pop("choices")

        parser.add_argument(*name_or_flags, **kwargs)

    def check_valid_assignment(self, value: T) -> None:
        """Determine whether the given value is an acceptable, valid assignment for this argument."""
        for validator, message in self.validators:
            if not validator(value):
                raise ValueError(message)
