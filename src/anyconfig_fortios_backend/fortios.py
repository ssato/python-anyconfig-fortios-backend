#
# Copyright (C) 2020 - 2023 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
r"""Very experimental parser parses fortios configuration.

- Format to support: Fortios' "show *configuration" outputs
- Requirements: None
- Development Status :: 4 - Beta
- Limitations:

  - Load function only and it doesn't support dump function
  - It should have some more I'm not aware of

Chnagelog:

    .. versionchanged:: 0.1.5

       Support multiple VDoms, workaround for corrupt outputs without correct
       indents and edit section ends without 'next' end marker.

    .. versionadded:: 0.1.0
"""
import collections
import itertools
import re

import anyconfig.backend.base


DEF_DICT = collections.OrderedDict

EMPTY_RE = re.compile(r"^\s+$")
COMMENT_RE = re.compile(r"^\s*#(.*)$")

WORD_RE_S = r'(?:([^" \t\n\r\f\v]+)|"([^"]+)")'

# Examples:
# - 'config firewall address'
# - '       config ftgd-wf'
# - '            config filters'
CONFIG_START_RE = re.compile(r"^\s*"
                             r"config\s+"
                             r"(.+)$")
CONFIG_END_RE = re.compile(r"^\s*end$")

# Examples:
# - '     edit "fortinet"'
# - '            edit 1'
EDIT_START_RE = re.compile(r"^(\s*)"
                           r"edit\s+"
                           + WORD_RE_S +
                           r"$")
EDIT_END_RE = re.compile(r"^\s*next$")

SET_OR_UNSET_LINE_RE = re.compile(r"^\s*"
                                  r"(set|unset)\s+"
                                  r"(\S+)\s*"
                                  r"(.+)*$")
SET_VALUE_RE = re.compile(WORD_RE_S + r"\s*")


def process_config_or_edit_line(matched):
    """
    :param matched: :class:`re.Match` object holding the config line info

    :raises: ValueError
    :return: A str gives the name of this config or edit
    """
    matches = matched.groups()
    if len(matches) > 1:  # edit
        vals = [m for m in matches[1:] if m][0]
    else:
        vals = matches[0]

    return vals


def process_set_or_unset_line(matched, container=DEF_DICT):
    """
    :param matched: :class:`re.Match` object holding the '*set' line info
    :param container: Constructor to make mapping objects [OrderedDict]

    :raises: ValueError
    :return: A tuple of (name, type, *args)
    """
    matches = [m for m in matched.groups() if m is not None]
    if len(matches) < 2:
        msg = "line: {}, matches: {}".format(matched.string,
                                             ", ".join(matches))
        raise ValueError(msg)

    if len(matches) == 2:  # ex. unset ssd-trim-weekday
        return container(type=matches[0], name=matches[1])

    vss = SET_VALUE_RE.findall(matches[2])
    values = [m for m in itertools.chain.from_iterable(vss) if m]

    return container(type=matches[0], name=matches[1], values=values)


(NT_CONFIG, NT_EDIT) = ("config", "edit")


def make_node(matched, type_=None):
    """
    :param matched: :class:`re.Match` object holding the config line info
    :param type_: Node type

    :return: A collections.namedtuple object has a config or edit info
    """
    if type_ is None:
        type_ = NT_CONFIG

    name = process_config_or_edit_line(matched)
    end_re = CONFIG_END_RE if type_ == NT_CONFIG else EDIT_END_RE

    Node = collections.namedtuple(type_.title(),
                                  ("name", "type", "end_re", "children"))
    return Node(name=name, type=type_, end_re=end_re, children=[])


CNF_NAME = CNF_TYPE = "config"
EDIT_NAME = EDIT_TYPE = "edit"


def _process_vals(vals):
    """
    :param vals: None or a single value in a list of a list

    >>> _process_vals(None) is None
    True
    >>> _process_vals([])
    []
    >>> _process_vals([0])
    0
    >>> _process_vals(["0", "1"])
    ['0', '1']
    """
    if vals is None or not vals:
        return vals

    if len(vals) == 1:  # single value in a list
        return vals[0]

    return vals


def node_to_dict(node, verbose=False, container=DEF_DICT):
    """Convert a Node namedtuple object to a dict.

    :param verbose: return verbose dict if True
    :param container: Constructor to make mapping objects [OrderedDict]
    """
    if verbose:
        return container(name=node.name, type=node.type,
                         children=node.children)

    ccnfs = [c for c in node.children if CNF_NAME in c]  # config in children
    cedits = [e for e in node.children if EDIT_NAME in e]  # edit in children

    # set or unset in children
    cmaps = container((x["name"], _process_vals(x.get("values", None)))
                      for x in node.children
                      if x.get("type") in ("set", "unset"))
    if ccnfs:
        cmaps["configs"] = ccnfs

    if cedits:
        cmaps["edits"] = cedits

    if node.type == EDIT_TYPE:
        return container(edit=node.name, **cmaps)

    return container(config=node.name, **cmaps)


def _process_comment(content, container=DEF_DICT):
    """
    Parse comment content, make a mapping objects and return it.

    :param content: A str represents a comment
    :param container: Constructor to make mapping objects [OrderedDict]

    :return: A mapping object made by parsing a comment
    """
    return container(kv.split('=') for kv in content.split(':'))


def is_config_or_edit_end(line, configs):
    """
    Is the line indicates that 'config' or 'edit' section ends?

    - config <name>
        ...
      end

    - edit <name>
        ...
      next

    :param line: A str represents a line in configurations output
    :param configs: A stack (list) holding config node objects
    """
    if configs[-1].end_re.match(line):  # config/edit section ends.
        return True

    return False


def is_edit_end_without_next(line, configs):
    """
    Is the line indicates that 'edit' section ends without 'next' end marker
    (special case)?

    - config vdom
      edit <name>
        ...
      end

    :param line: A str represents a line in configurations output
    :param configs: A stack (list) holding config node objects
    """
    if len(configs) > 1:
        (parent, child) = (configs[-2], configs[-1])  # (config, edit)
        if parent.end_re.match(line) and parent.name == "vdom" and \
                parent.type == NT_CONFIG and child.type == NT_EDIT:
            return True

    return False


# pylint: disable=too-many-branches,too-many-statements
def parse_show_config_itr(stream, container=DEF_DICT, verbose=False):
    """
    Parse 'config xxxxx xxxx' .. 'end'.

    :param stream: An iterator yields each lines in configuration outputs
    :param container: object to hold results
    :param verbose: return verbose result if True
    """
    configs = []  # stack holds nested config objects
    ntdopts = dict(verbose=verbose, container=container)

    # A mapping object holds comments; There are not so many comments.
    comments = container(comments=[])

    for line in stream:
        if EMPTY_RE.match(line):
            continue

        matched = COMMENT_RE.match(line)
        if matched:
            content = matched.groups()[0].strip()
            comments["comments"].append(content)
            try:
                comments.update(_process_comment(content, container=container))
            except ValueError:
                pass  # content does not contain structured data.

            continue  # Don't yield it here. Maybe there're another ones.

        matched = CONFIG_START_RE.match(line)
        if matched:
            config = make_node(matched)
            configs.append(config)  # push this config.
            continue

        matched = EDIT_START_RE.match(line)
        if matched:
            edit = make_node(matched, type_=NT_EDIT)
            configs.append(edit)  # push this edit.
            continue

        matched = SET_OR_UNSET_LINE_RE.match(line)
        if matched:
            set_val = process_set_or_unset_line(matched, container=container)
            configs[-1].children.append(set_val)
            continue

        if configs:
            if is_config_or_edit_end(line, configs):
                dic = node_to_dict(configs.pop(), **ntdopts)
                if not configs:  # It's a top level config.
                    yield dic
                else:
                    configs[-1].children.append(dic)

            elif is_edit_end_without_next(line, configs):
                edit = node_to_dict(configs.pop(), **ntdopts)
                node = configs.pop()
                node.children.append(edit)

                cnf = node_to_dict(node, **ntdopts)
                if not configs:  # It's a top level config.
                    yield cnf
                else:
                    configs[-1].children.append(cnf)

    if comments["comments"]:
        if verbose:
            comments["type"] = comments["name"] = "comment"  # TBD
        yield comments


def load(stream, container=DEF_DICT):
    """
    Load and parse Java properties file given as a fiel or file-like object
    'stream'.

    :param stream:
        A file or file like object of fortigate "show *configuration" outputs
    :param container:
        Factory function to create a dict-like object to store configurations

    :return: A mapping object holding fortios' configurations
    """
    cnfs = list(parse_show_config_itr(stream, container=container))
    return container(configs=cnfs)


class Parser(anyconfig.backend.base.Parser,
             anyconfig.backend.base.FromStreamLoaderMixin):
    """
    Loader for fortios (fortigate) "show *configuration" outputs.
    """
    _cid = "fortios"
    _type = "fortios"
    _extensions = []
    _load_opts = ["full"]
    _ordered = True

    def load_from_stream(self, stream, container, **kwargs):
        """
        Load config from given file or file-like object `stream`.

        :param stream: A file or file like object of Java properties files
        :param container: callble to make a container object
        :param kwargs: optional keyword parameters (ignored)

        :return: Dict-like object holding config parameters
        """
        return load(stream, container=container)

    def dump_to_stream(self, cnf, stream, **kwargs):
        """
        Dump config 'cnf' to a file or file-like object 'stream'.

        :param cnf: Java properties config data to dump
        :param stream: Java properties file or file like object
        :param kwargs: backend-specific optional keyword parameters :: dict
        """
        raise NotImplementedError("Not implemented yet")

# vim:sw=4:ts=4:et:
