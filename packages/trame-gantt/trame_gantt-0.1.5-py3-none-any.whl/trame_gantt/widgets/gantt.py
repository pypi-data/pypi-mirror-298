"""Module compatible with vue3. To use it, you need to install **trame-gantt**"""
from trame_client.widgets.core import AbstractElement
from .. import module

__all__ = [
    "Gantt",
]


class HtmlElement(AbstractElement):
    def __init__(self, _elem_name, children=None, **kwargs):
        super().__init__(_elem_name, children, **kwargs)
        if self.server:
            self.server.enable_module(module)

class Gantt(HtmlElement):
    """
    Gantt Editor component

    Properties:

    :param items:
    :param title:
    :param fields:
    :param levels:
    :param dateLimit:
    :param startDate:
    :param endDate:
    :param canEdit:

    """

    def __init__(self, **kwargs):
        super().__init__(
            "gantt",
            **kwargs,
        )
        self._attr_names += [
            "items",
            "title",
            "fields",
            "levels",
            "dateLimit",
            "startDate",
            "endDate",
            "canEdit"
        ]
        self._event_names += [
            "input",
            "update"
        ]
