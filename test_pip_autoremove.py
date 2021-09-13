import subprocess

import pkg_resources

import pip_autoremove


def test_find_all_dead():
    graph = {
        "Flask": set(),
        "Jinja2": {"Flask", "Sphinx"},
        "MarkupSafe": {"Jinja2"},
        "Werkzeug": {"Flask"},
        "itsdangerous": {"Flask"},
        "Sphinx": set(),
        "pip": set(),
        "setuptools": set(),
    }
    start = {"Flask"}
    expected = {"Flask", "Werkzeug", "itsdangerous"}
    dead = pip_autoremove.find_all_dead(graph, start)
    assert dead == expected

    start = {"Sphinx"}
    dead = pip_autoremove.find_all_dead(graph, start)
    assert dead == start

    start = {"Sphinx", "Flask"}
    expected = {"Flask", "Werkzeug", "itsdangerous", "Sphinx", "Jinja2", "MarkupSafe"}
    dead = pip_autoremove.find_all_dead(graph, start)
    print(dead)
    assert dead == expected


def install_dist(req):
    subprocess.check_call(["pip", "install", req])


def has_dist(req):
    req = pkg_resources.Requirement.parse(req)
    working_set = pkg_resources.WorkingSet()
    return working_set.find(req)


def test_main():
    expected = ["Flask", "Jinja2", "MarkupSafe", "Werkzeug", "itsdangerous"]

    install_dist("Flask")
    for name in expected:
        assert has_dist(name)

    pip_autoremove.main(["-y", "Flask"])
    for name in expected:
        assert not has_dist(name)
