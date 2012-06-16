import sublime, sublime_plugin, os

class GotoOpenFileCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    window = sublime.active_window()
    views = window.views()

    selector = ViewSelector(window, views)
    
    window.show_quick_panel(selector.get_items(), selector.select)

class ViewSelector(object):

  def __init__(self, window, views):
    self.window = window
    self.views = views

  def select(self, index):
    if index != -1:
      self.window.focus_view(self.views[index])

  def get_items(self):
    return [[os.path.basename(view.file_name()), self.__get_path(view)] for view in self.views]

  def __get_path(self, view):
    folders = self.window.folders()

    for folder in folders:
      if os.path.commonprefix([folder, view.file_name()]) == folder:
        relpath = os.path.relpath(view.file_name(), folder)
        
        if len(folders) > 1:
          return os.path.join(os.path.basename(folder), relpath)

        return relpath

    return view.file_name()
    