from nicetrace import trace, FileWriter
import time

with FileWriter("traces/my_trace.json"):
    with trace("Root node"):
        while True:
            print(".")
            time.sleep(1)
            with trace("Child node", inputs={"x": 10, "y": 20}) as node:
                node.add_output("", "Hello world!")
