# Format .scala files with scalariform.
#
# Author: Christopher Swenson (chris@caswenson.com)

from threading import Lock
import sublime, sublime_plugin
import subprocess as sp

patterns = ['swenson@simple.com', 'chris@caswenson.com']

SCALARIFORM_JAR = "/Users/swenson/Downloads/scalariform.jar"
SCALARIFORM_OPTIONS = "-indentSpaces=2 +doubleIndentClassDeclaration +alignParameters"

def new_scalariform():
  return sp.Popen("java -jar %s %s --stdin --stdout" % (SCALARIFORM_JAR, SCALARIFORM_OPTIONS),
    shell=True, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)

lock = Lock()
# Use a list to avoid problems with scope
scalariform = [new_scalariform()]

def format_scala(text):
  with lock:
    stdout, stderr = scalariform[0].communicate(bytes(text, "UTF-8"))
    scalariform[0] = new_scalariform()
    return str(stdout, "UTF-8")

class SwensonFormatScala(sublime_plugin.EventListener):
  def on_pre_save(self, view):
    if view.file_name().endswith(".scala"):
      if any(view.find(pattern, 0, sublime.IGNORECASE) for pattern in patterns):
        print("Formatting scala file %s" % view.file_name())
        new = view.substr(sublime.Region(0, view.size()))
        formatted = format_scala(new)
        if formatted.strip() != '':
          view.run_command("replace_text", dict(formatted=formatted))

class ReplaceTextCommand(sublime_plugin.TextCommand):
  def run(self, edit, formatted=""):
    self.view.replace(edit, sublime.Region(0, self.view.size()), formatted)
