# Format .scala files with scalariform.
#
# Author: Christopher Swenson (chris@caswenson.com)

import os.path
from threading import Lock
import sublime, sublime_plugin
import subprocess as sp

def new_scalariform(jar, options):
  return sp.Popen("java -jar %s %s --stdin --stdout" % (jar, options),
    shell=True, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)

lock = Lock()
# Use a list to avoid problems with scope
scalariform = []

def format_scala(text, jar, options):
  with lock:
    if not scalariform:
      scalariform.append(new_scalariform(jar, options))

    stdout, stderr = scalariform[0].communicate(text.encode("UTF-8"))
    scalariform[0] = new_scalariform(jar, options)
    return stdout.decode("UTF-8")

class SwensonFormatScala(sublime_plugin.EventListener):
  def on_pre_save(self, view):
    settings = sublime.load_settings('Preferences.sublime-settings')
    jar = settings.get("scalariform_jar", '~/scalariform.jar')
    options = settings.get("scalariform_options", "-indentSpaces=2 +alignParameters +doubleIndentClassDeclaration")
    if not os.path.exists(jar):
      print("Could not find scalariform.jar")
      return

    if view.file_name().endswith(".scala"):
      print("Formatting scala file %s" % view.file_name())
      new = view.substr(sublime.Region(0, view.size()))
      formatted = format_scala(new, jar, options)
      if formatted.strip() != '':
        view.run_command("replace_text", dict(formatted=formatted))

class ReplaceTextCommand(sublime_plugin.TextCommand):
  def run(self, edit, formatted=""):
    self.view.replace(edit, sublime.Region(0, self.view.size()), formatted)
