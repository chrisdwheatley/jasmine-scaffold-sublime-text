import os
import sys
import sublime
import sublime_plugin

directory = os.path.dirname(os.path.realpath(__file__))
src_path = os.path.join(directory, "src")
is_py2k = sys.version_info < (3, 0)

# Python 2.x on Windows can't properly import from non-ASCII paths, so
# this code added the DOC 8.3 version of the lib folder to the path in
# case the user's username includes non-ASCII characters
# logic take  from jsFormat plugin (https://github.com/jdc0589/JsFormat)
def add_lib_path(lib_path):
	def _try_get_short_path(path):
		path = os.path.normpath(path)
		if is_py2k and os.name == 'nt' and isinstance(path, unicode):
			try:
				import locale
				path = path.encode(locale.getpreferredencoding())
			except:
				from ctypes import windll, create_unicode_buffer
				buf = create_unicode_buffer(512)
				if windll.kernel32.GetShortPathNameW(path, buf, len(buf)):
					path = buf.value
		return path
	lib_path = _try_get_short_path(lib_path)
	if lib_path not in sys.path:
		sys.path.append(lib_path)

add_lib_path(src_path)

from transform import transform

class JasmineScaffoldCommand(sublime_plugin.TextCommand):

	# whether tabs are being translated to spaces or not
	# @return {bool}
	def translatingTabsToSpaces(self):
		return self.view.settings().get('translate_tabs_to_spaces')

	# counts the spacing being used
	# @return {int}
	def spacingSetting(self):
		return self.view.settings().get('tab_size')

	# main, triggered when shortcut keys are pressed
	def run(self, edit):
		lines = []

		# create a region from the first sel to the last
		region = sublime.Region(0, self.view.size())
		file = self.view.substr(region)

		# create an array of lines
		for line in file.splitlines():
			lines.append(line)

		# build the scaffolded tests, either for tab or space settings
		if self.translatingTabsToSpaces():
			scaffolded = transform().buildScaffold(lines, self.spacingSetting(), ' ', True)
		else:
			scaffolded = transform().buildScaffold(lines, self.spacingSetting(), '\t', False)	

		# replace the whole view with the joined array we've just created
		self.view.replace(edit, region, ''.join(scaffolded))
