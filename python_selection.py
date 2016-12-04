import sublime
import sublime_plugin

import functools
import string
import math
import re

EXPORTED_MODULES = [string, math, re]


class PythOnSelectionEvalCommand(sublime_plugin.WindowCommand):

    """
    Standard ST plugin initialization taken from
    http://docs.sublimetext.info/en/latest/extensibility/plugins.html
    """

    def run(self):
        self.window.show_input_panel(
            "Enter Python expression (v: value, i: index)",
            "",
            self.done,
            None,
            None
        )

    def done(self, expr):
        view = self.window.active_view()
        view.run_command("pyth_on_selection_eval_on_each_line", {"expr": expr})


class PythOnSelectionEvalOnEachLineCommand(sublime_plugin.TextCommand):

    def eval(self, expr):
        """
        Yield the result of the given expression. The resulting generator
        accepts a send() with the current value of the selection.
        """

        def format(s, adict):
            return s.format(**adict)

        local_variables = {m.__name__: m for m in EXPORTED_MODULES}

        f = functools.partial(format, adict=local_variables)

        value = yield

        for idx in range(len(self.view.sel())):
            local_variables.update({
                '_': ' ',
                'f': f,
                'i': idx,
                'si': str(idx),
                'l': len(value),
                'sl': str(len(value)),
                'v': value,
            })

            value = yield str(eval(expr, local_variables))

    def run(self, edit, expr=None):
        if not expr:
            return

        g = self.eval(expr)
        next(g)

        for selection in self.view.sel():
            s = self.view.substr(selection)

            self.view.replace(edit, selection, g.send(s))


class PythOnSelectionFormatCommand(sublime_plugin.WindowCommand):

    """
    Standard ST plugin initialization taken from
    http://docs.sublimetext.info/en/latest/extensibility/plugins.html
    """

    def run(self):
        self.window.show_input_panel(
            "Enter format expression (v: value, i: index)",
            "",
            self.done,
            None,
            None
        )

    def done(self, expr):
        view = self.window.active_view()
        view.run_command("pyth_on_selection_format_each_line", {"expr": expr})


class PythOnSelectionFormatEachLineCommand(sublime_plugin.TextCommand):

    def eval(self, expr):
        """
        Yield the result of the given format expression. The resulting
        generator accepts a send() with the current value of the selection.
        """

        local_variables = {m.__name__: m for m in EXPORTED_MODULES}

        value = yield

        for idx in range(len(self.view.sel())):
            local_variables.update({
                'i': idx,
                'l': len(value),
                'v': value,
            })

            value = yield str(expr).format(**local_variables)

    def run(self, edit, expr=None):
        if not expr:
            return

        g = self.eval(expr)
        next(g)

        for selection in self.view.sel():
            s = self.view.substr(selection)

            self.view.replace(edit, selection, g.send(s))
