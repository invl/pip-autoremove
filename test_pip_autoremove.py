import pip
import pkg_resources

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


def install_dist(req):
    pip.main(['install', req])
    pip.logger.consumers = []


def has_dist(req):
    req = pkg_resources.Requirement.parse(req)
    working_set = pkg_resources.WorkingSet()
    return working_set.find(req)


def test_main():
    expected = ["Flask", "Jinja2", "MarkupSafe", "Werkzeug", "itsdangerous"]

    install_dist('Flask')
    for name in expected:
        assert has_dist(name)

    pip_autoremove.main(['-y', 'Flask'])
    for name in expected:
        assert not has_dist(name)
