import sublime, sublime_plugin

import re
import os
import json
import fnmatch
import StringIO
import contextlib

import cmd_parser

import sublime_lib.view as vlib
from sublime_lib.view import append


TOKEN_TARGET_APPLICATION = 0
TOKEN_TARGET_WINDOW = 1
TOKEN_TARGET_VIEW = 2

TOKEN_ACTION_QUERY = 3
TOKEN_ACTION_EXECUTE = 4

TOKEN_OPTION_FORCE = 5


def equals_any(what, seq, comp_func=None):
    """Compares what with seq and returns matching elements according to
    comp_func. comp_func defaults to an equality comparison.
    """
    if comp_func is None: comp_func = lambda x: x == what
    return filter(comp_func, seq)


def gen_files(package_name, include, exclude=('.hg', '.svn', '.git')):
    target = os.path.abspath(os.path.join(
                                   sublime.packages_path(),
                                   package_name))
   
    for base, dirs, files in os.walk(target):
        if equals_any(base, exclude): continue
        for f in files:
            match = equals_any(f, include)
            if match:
                yield base, match[0]
            

def in_merge_order(include, **kwargs):
    for dirname in ('Default', '', 'User'):
        for base, f in gen_files(dirname, include, **kwargs):
            if dirname == '' and (base.endswith('Default') or
                                  base.endswith('User')):
                continue
            yield os.path.join(base, f)


def strip_comments(json_fname):
    with open(json_fname) as fh:
        lines = fh.readlines()
        for i, line in enumerate(lines):
            if "//" in line:
                lines[i] = re.sub("//.*$", '', line)
    return lines


def get_merged_settings(fname):
    merged_settings = {}
    # Order isn't correct if a settings file name starts lower than Base File.
    # Maybe order settings once collected?
    for f in in_merge_order(('Base File.sublime-settings', fname)):
        lines = strip_comments(f)
        fake_fh = StringIO.StringIO('\n'.join(lines))
        settings_raw = json.load(fake_fh)
        for k,v in settings_raw.iteritems():
            if k in merged_settings:
                merged_settings[k].append((f, v))
            else:
                merged_settings[k] = [(f, v)]
 
    return merged_settings


def to_json_type(v):
    """"Convert string value to proper JSON type.
    """
    try:
        if v.lower() in ("false", "true"):
            v = (True if v.lower() == "true" else False)
        elif v.isdigit():
            v = int(v)
        elif v.replace(".", "").isdigit():
            v = float(v)
    except AttributeError:
        raise ValueError("Conversion to JSON failed for: %s" % v)

    return v


class SublimeCmdCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.window = self.view.window()
        v = self.window.show_input_panel('Sublime CMD:',
                                    '',
                                    self.on_done, None, None)
        # Remember last command.
        content = getattr(self, 'last_cmd', '')
        if content:
            append(v, content)
            v.sel().add(sublime.Region(0, v.size()))

    def on_done(self, s):
        self.last_cmd = s
        cmd_parser.parse_and_dispatch(self.view, s)


class InspectFileSettingsCommand(sublime_plugin.TextCommand):
    def run(self, edit, syntax, pattern):
        settings_name, _ = os.path.splitext(syntax)
        settings = get_merged_settings(settings_name + '.sublime-settings')

        out_view = self.view.window().new_file()
        out_view.set_scratch(True)

        vlib.append(out_view, "=" * 79 + "\n")
        vlib.append(out_view, "Settings for: %s\n" % self.view.file_name())
        vlib.append(out_view, "-" * 79)
        vlib.append(out_view, '\n')

        for k, v in settings.iteritems():
            if fnmatch.fnmatch(k, pattern):
                vlib.append(out_view, k + ":\n")
                last = None
                for location, value in v:
                    location = location[location.find('Packages'):]
                    vlib.append(out_view, "\t%s\t\t\t%s\n" % (value, location))
                    last = value
                session_value = self.view.settings().get(k)
                if session_value != last:
                    vlib.append(out_view, "\t%s\t\t\t%s\n" % _
                                    (self.view.settings().get(k), "Session"))
                vlib.append(out_view, '\n')
        vlib.append(out_view, "=" * 79)


class GetAllCommandsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        all_ = sublime_plugin.all_command_classes
        all_cmds = []
        for gr in all_:
            for cmd in gr:
                cli = "run" if issubclass(cmd, sublime_plugin.TextCommand) else "run:w"
                all_cmds.append("%s\t%s" % (cli, cmd.__name__))
        
        txt = '\n'.join(sorted(all_cmds))
        txt = re.sub(r"([a-z])([A-Z])", r"\1_\2", txt).lower()
        txt = re.sub(r"(.*)_command", r"\1", txt)

        v = self.view.window().new_file()
        v.set_scratch(True)
        vlib.append(v, txt)