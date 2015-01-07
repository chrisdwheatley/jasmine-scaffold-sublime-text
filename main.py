import sublime
import sublime_plugin

class JasmineScaffoldCommand(sublime_plugin.TextCommand):

    # whether tabs are being translated to spaces or not
    # return [bool]
	def translatingTabsToSpaces(self):
		return self.view.settings().get('translate_tabs_to_spaces')

	# counts the spacing being used
	# return [int]
	def spacingSetting(self):
		return self.view.settings().get('tab_size')

	# count the number of whitespace characters at the start of each line
	# return [int]
	def countLineWhitespace(self, line, type):
		return len(line) - len(line.lstrip(type))

	# param [list] lines read from file in focus
	# param [int] spacingCount tab/space size
	# param [str] spacingType space or tab character
	# param [bool] usingSpaces current user setting, spaces or tabs
	# todo refactor out into smaller chunks
	# return [list] scaffold
	def buildScaffold(self, lines, spacingCount, spacingType, usingSpaces):
		scaffold = []

		for index, line in enumerate(lines):
			currentWhitespace = self.countLineWhitespace(line, spacingType)

			if index < len(lines) - 1:
				nextWhitespace = self.countLineWhitespace(lines[index + 1], spacingType)
			else:
				nextWhitespace = 0

			descRepl = 'describe(\'' + line.lstrip(spacingType) + '\', function() {\n\n'
			indented = descRepl.rjust(len(descRepl) + currentWhitespace, spacingType)

			if currentWhitespace > nextWhitespace:
				itRepl = 'it(\'' + line.lstrip(spacingType) + '\', function() {\n\n'
				copy = currentWhitespace
				indented = []

				indented.append(itRepl.rjust(len(itRepl) + currentWhitespace, spacingType) + '});'.rjust(3 + currentWhitespace, spacingType) + '\n\n')
				while copy > nextWhitespace:
					copy -= spacingCount if usingSpaces else 1
					closeBrackets = '});'.rjust(3 + copy, spacingType) + '\n\n'
					indented.append(closeBrackets)

			scaffold.extend(indented)

		return scaffold

	# main
	def run(self, edit):
		lines = []

		# create a region from the first sel to the last
		region = sublime.Region(0, self.view.size())
		file = self.view.substr(region)

		# create an array of lines
		for line in file.splitlines():
			lines.append(line)

		if self.translatingTabsToSpaces():
			scaffolded = self.buildScaffold(lines, self.spacingSetting(), ' ', True)
		else:
			scaffolded = self.buildScaffold(lines, self.spacingSetting(), '\t', False)	

		# replace the whole view with the joined array we've just created
		self.view.replace(edit, region, ''.join(scaffolded))
