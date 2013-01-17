# Format .scala files with scalariform.
#
# Author: Christopher Swenson (chris@caswenson.com)

import sublime, sublime_plugin
import subprocess as sp

SCALARIFORM_JAR = "/Users/swenson/Downloads/scalariform.jar"
SCALARIFORM_OPTIONS = "-indentSpaces=2 +doubleIndentClassDeclaration"

def format_scala(text):
  p = sp.Popen("java -jar %s %s --stdin --stdout" % (SCALARIFORM_JAR, SCALARIFORM_OPTIONS),
    shell=True, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
  stdout, stderr = p.communicate(text)
  return stdout

class SwensonFormatScala(sublime_plugin.EventListener):
  def on_pre_save(self, view):
    if view.file_name().endswith(".scala"):
      print "Formatting scala file %s" % view.file_name()
      new = view.substr(sublime.Region(0, view.size()))
      formatted = format_scala(new)
      edit = view.begin_edit()
      view.replace(edit, sublime.Region(0, view.size()), formatted)
      view.end_edit(edit)
