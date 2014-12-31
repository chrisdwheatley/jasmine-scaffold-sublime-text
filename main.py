import sublime
import sublime_plugin

class JasmineScaffoldCommand(sublime_plugin.TextCommand):

    # whether tabs are being translated to spaces or not
    # return boolean
	def translatingTabsToSpaces(self):
		return self.view.settings().get('translate_tabs_to_spaces')

	# counts the spacing being used
	# return int
	def spacingSetting(self):
		return self.view.settings().get('tab_size')

	# count the number of whitespace characters at the start of each line
	# return int
	def countLineWhitespace(self, line, type):
		return len(line) - len(line.lstrip(type))

	def buildScaffold(self, lines, spacingCount, spacingType):
		scaffold = []

		for index, line in enumerate(lines):
			currentWs = self.countLineWhitespace(line, spacingType)

			if index < len(lines) - 1:
				nextWs = self.countLineWhitespace(lines[index + 1], spacingType)
			else:
				nextWs = 0

			replacement = 'describe(\'' + line.lstrip(spacingType) + '\', function() {\n\n'
			indented = replacement.rjust(len(replacement) + currentWs, spacingType)

			if currentWs > nextWs:
				replacement = 'it(\'' + line.lstrip(spacingType) + '\', function() {\n\n'
				copy = currentWs
				indented = []

				indented.extend(replacement.rjust(len(replacement) + currentWs, spacingType) + '});'.rjust(3 + currentWs, spacingType) + '\n\n')

				while copy > nextWs:
					copy -= spacingCount
					closeBrackets = '});'.rjust(3 + copy, spacingType) + '\n\n'
					indented.extend(closeBrackets)

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
			scaffolded = self.buildScaffold(lines, self.spacingSetting(), ' ')
		else:
			scaffolded = self.buildScaffold(lines, self.spacingSetting(), '\t')

		# replace the whole view with the joined array we've just created
		self.view.replace(edit, region, ''.join(scaffolded))
