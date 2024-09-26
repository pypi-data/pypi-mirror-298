import time
from nicetrace import trace, DirWriter, write_html

with DirWriter("traces"):
    with trace("Root", inputs={"x": 10, "y": 20}):
        with trace("Child 1") as x:
            x.add_output("", "Hello!")
        with trace("Child 2"):
            pass


from nicetrace import trace, FileWriter

with FileWriter("traces/my_trace.json"):
    with trace("Root node"):
        with trace("Child node", inputs={"x": 10, "y": 20}) as node:
            node.add_output("", "Hello world!")


from nicetrace import trace

with trace("my node", inputs={"x": 42}) as node:
    node.add_output("y", "my_result")

import json

print(json.dumps(node.to_dict(), indent=2))


from dataclasses import dataclass
from nicetrace import trace, with_trace


@dataclass
class Person:
    name: str
    age: int


@with_trace
def say_hi(person):
    return f"Hi {person.name}!"


with trace("root") as c:
    person = Person("Alice", 21)
    say_hi(person)

print(json.dumps(c.to_dict(), indent=2))
