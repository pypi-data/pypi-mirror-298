from trame_gantt.widgets.gantt import *


def initialize(server):
    from trame_gantt import module

    server.enable_module(module)