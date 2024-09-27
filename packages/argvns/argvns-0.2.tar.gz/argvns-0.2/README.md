# argvns

This package is designed to provide a wrapper around `argparse` in order to provide static typing information to the
parsed arguments. This also allows for autocomplete and context actions for the arguments.

It replaces something like

```python
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from typing import Self


@dataclass
class Config:
    name: str
    age: int
    jobs: list[str]

    @classmethod
    def from_argv(cls, args: list[str] | None = None, namespace: Namespace | None = None) -> Self:
        parser = ArgumentParser()
        parser.add_argument("-n", "--name", help="the name of the person")
        parser.add_argument("-a", "--age", type=int, help="the age of the person")
        parser.add_argument("-j", "--jobs", nargs="*", help="the person's jobs")

        parsed = parser.parse_args(args, namespace)
        return cls(**vars(parsed))


def main():
    config = Config.from_argv()
```

which requires defining the keys twice and is just annoying boilerplate. It becomes

```python
from argvns import argvns, Arg


@argvns
class Config:
    name: str = Arg(short="-n", long="--name", help="the name of the person")
    age: int = Arg(short="-a", long="age", type=int, help="the age of the person")
    jobs: list[str] = Arg(short="-j", long="--jobs", nargs="+", help="the person's jobs")


def main():
    config = Config()
```

Because `argvns` is a thin wrapper around `argparse`, it uses the same arguments and semantics for the `Arg` constructor
that `ArgumentParser.add_argument` does. 