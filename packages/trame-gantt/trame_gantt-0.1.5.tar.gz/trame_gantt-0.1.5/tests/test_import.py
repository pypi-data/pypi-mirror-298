def test_import():
    from trame_gantt.widgets.gantt import Gantt  # noqa: F401

    # For components only, the CustomWidget is also importable via trame
    from trame.widgets.gantt import Gantt  # noqa: F401,F811
