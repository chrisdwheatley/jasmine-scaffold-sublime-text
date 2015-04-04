import sublime
import sublime_plugin

class JasmineScaffoldCommand(sublime_plugin.TextCommand):

	DESCRIBE_LINE = 'describe(\'%s\', function() {\n\n'
	IT_LINE = 'it(\'%s\', function() {\n\n'

	# whether tabs are being translated to spaces or not
	# @return {bool}
	def translatingTabsToSpaces(self):
		return self.view.settings().get('translate_tabs_to_spaces')

	# counts the spacing being used
	# @return {int}
	def spacingSetting(self):
		return self.view.settings().get('tab_size')

	# count the number of whitespace characters at the start of each line
	# @return {int}
	def countLineWhitespace(self, line, type):
		return len(line) - len(line.lstrip(type))

	# build an array of lines to output
	# @todo refactor out into smaller chunks
	# @param {list} lines read from file in focus
	# @param {int} spacingCount tab/space size
	# @param {str} spacingType space or tab character
	# @param {bool} usingSpaces current user setting, spaces or tabs
	# @return {list} scaffold
	def buildScaffold(self, lines, spacingCount, spacingType, usingSpaces):
		scaffold = []

		for index, line in enumerate(lines):
			lineText = line.lstrip(spacingType)
			currentWhitespace = self.countLineWhitespace(line, spacingType)

			if index < len(lines) - 1:
				nextWhitespace = self.countLineWhitespace(lines[index + 1], spacingType)
			else:
				nextWhitespace = self.countLineWhitespace(lines[0], spacingType)

			descRepl = self.DESCRIBE_LINE % lineText
			indented = descRepl.rjust(len(descRepl) + currentWhitespace, spacingType)

			if currentWhitespace >= nextWhitespace:
				itRepl = self.IT_LINE % lineText
				decreasingWhitespace = currentWhitespace
				indented = []

				indented.append(itRepl.rjust(len(itRepl) + currentWhitespace, spacingType) + '});'.rjust(3 + currentWhitespace, spacingType) + '\n\n')
				while decreasingWhitespace > nextWhitespace:
					decreasingWhitespace -= spacingCount if usingSpaces else 1
					closeBrackets = '});'.rjust(3 + decreasingWhitespace, spacingType) + '\n\n'
					indented.append(closeBrackets)

			scaffold.extend(indented)

		return scaffold

	# get the start of a selected region
	def getSelectedRegionStart(self, view, point):
		lineRegion = view.line(point)
		pos = lineRegion.a
		end = lineRegion.b
		while pos < end:
			ch = view.substr(pos)
			if ch != self.spacingSetting():
				break
			pos += 1
		return pos

	# main, triggered when shortcut keys are pressed
	def run(self, edit):
		lines = []

		# create a region from the first sel to the last
		if len(self.view.sel()[0]) == 0:
			region = sublime.Region(0, self.view.size())
		else:
			for sel in self.view.sel():
				start = self.getSelectedRegionStart(self.view, min(sel.a, sel.b))
				region = sublime.Region(self.view.line(start).a, self.view.line(max(sel.a, sel.b)).b)

		file = self.view.substr(region)

		# create an array of lines
		for line in file.splitlines():
			lines.append(line)

		# build the scaffolded tests, either for tab or space settings
		if self.translatingTabsToSpaces():
			scaffolded = self.buildScaffold(lines, self.spacingSetting(), ' ', True)
		else:
			scaffolded = self.buildScaffold(lines, self.spacingSetting(), '\t', False)

		# clear selected text
		self.view.sel().clear()

		# replace the whole view with the joined array we've just created
		self.view.replace(edit, region, ''.join(scaffolded))
