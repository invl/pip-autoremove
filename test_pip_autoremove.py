import pip_autoremove


def test_find_all_dead():
    graph = {
        'Flask': set([]),
        'Jinja2': set(['Flask']),
        'MarkupSafe': set(['Jinja2']),
        'Werkzeug': set(['Flask']),
        'itsdangerous': set(['Flask']),
        'pip': set([]),
        'setuptools': set([]),
    }
    start = set(["Flask"])
    expected = set(
        ["Flask", "Jinja2", "MarkupSafe", "Werkzeug", "itsdangerous"])
    dead = pip_autoremove.find_all_dead(graph, start)
    assert dead == expected
