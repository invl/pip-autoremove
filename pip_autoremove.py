from __future__ import print_function

import optparse
import subprocess
import sys
from collections import defaultdict

import pip
from pkg_resources import (
    DistributionNotFound,
    VersionConflict,
    get_distribution,
    working_set,
)

__version__ = "0.10.0"

try:
    raw_input
except NameError:
    raw_input = input

try:
    ModuleNotFoundError
except NameError:
    ModuleNotFoundError = ImportError

try:
    # pip >= 10.0.0 hides main in pip._internal. We'll monkey patch what we need and hopefully this becomes available
    # at some point.
    from pip._internal import logger, main

    pip.main = main
    pip.logger = logger
except (ModuleNotFoundError, ImportError):
    pass


WHITELIST = ["pip", "setuptools", "pip-autoremove", "wheel"]


def autoremove(names, yes=False):
    dead = list_dead(names)
    if dead and (yes or confirm("Uninstall (y/N)? ")):
        remove_dists(dead)


def list_dead(names):
    start = set()
    for name in names:
        try:
            start.add(get_distribution(name))
        except DistributionNotFound:
            print("%s is not an installed pip module, skipping" % name, file=sys.stderr)
        except VersionConflict:
            print(
                "%s is not the currently installed version, skipping" % name,
                file=sys.stderr,
            )
    graph = get_graph()
    dead = exclude_whitelist(find_all_dead(graph, start))
    for d in start:
        show_tree(d, dead)
    return dead


def exclude_whitelist(dists):
    return {dist for dist in dists if dist.project_name not in WHITELIST}


def show_tree(dist, dead, indent=0, visited=None):
    if visited is None:
        visited = set()
    if dist in visited:
        return
    visited.add(dist)
    print(" " * 4 * indent, end="")
    show_dist(dist)
    for req in requires(dist):
        if req in dead:
            show_tree(req, dead, indent + 1, visited)


def find_all_dead(graph, start):
    return fixed_point(lambda d: find_dead(graph, d), start)


def find_dead(graph, dead):
    def is_killed_by_us(node):
        succ = graph[node]
        return succ and not (succ - dead)

    return dead | set(filter(is_killed_by_us, graph))


def fixed_point(f, x):
    while True:
        y = f(x)
        if y == x:
            return x
        x = y


def confirm(prompt):
    return raw_input(prompt) == "y"


def show_dist(dist):
    print("%s %s (%s)" % (dist.project_name, dist.version, dist.location))


def show_freeze(dist):
    print(dist.as_requirement())


def remove_dists(dists):
    if sys.executable:
        pip_cmd = [sys.executable, "-m", "pip"]
    else:
        pip_cmd = ["pip"]
    subprocess.check_call(pip_cmd + ["uninstall", "-y"] + [d.project_name for d in dists])


def get_graph():
    g = defaultdict(set)
    for dist in working_set:
        g[dist]
        for req in requires(dist):
            g[req].add(dist)
    return g


def requires(dist):
    required = []
    for pkg in dist.requires():
        try:
            required.append(get_distribution(pkg))
        except VersionConflict as e:
            print(e.report(), file=sys.stderr)
            print("Redoing requirement with just package name...", file=sys.stderr)
            required.append(get_distribution(pkg.project_name))
        except DistributionNotFound as e:
            print(e.report(), file=sys.stderr)
            print("Skipping %s" % pkg.project_name, file=sys.stderr)
    return required


def main(argv=None):
    parser = create_parser()
    (opts, args) = parser.parse_args(argv)
    if opts.leaves or opts.freeze:
        list_leaves(opts.freeze)
    elif opts.list:
        list_dead(args)
    elif len(args) == 0:
        parser.print_help()
    else:
        autoremove(args, yes=opts.yes)


def get_leaves(graph):
    def is_leaf(node):
        return not graph[node]

    return filter(is_leaf, graph)


def list_leaves(freeze=False):
    graph = get_graph()
    for node in get_leaves(graph):
        if freeze:
            show_freeze(node)
        else:
            show_dist(node)


def create_parser():
    parser = optparse.OptionParser(
        usage="usage: %prog [OPTION]... [NAME]...",
        version="%prog " + __version__,
    )
    parser.add_option(
        "-l",
        "--list",
        action="store_true",
        default=False,
        help="list unused dependencies, but don't uninstall them.",
    )
    parser.add_option(
        "-L",
        "--leaves",
        action="store_true",
        default=False,
        help="list leaves (packages which are not used by any others).",
    )
    parser.add_option(
        "-y",
        "--yes",
        action="store_true",
        default=False,
        help="don't ask for confirmation of uninstall deletions.",
    )
    parser.add_option(
        "-f",
        "--freeze",
        action="store_true",
        default=False,
        help="list leaves (packages which are not used by any others) in requirements.txt format",
    )
    return parser


if __name__ == "__main__":
    main()
