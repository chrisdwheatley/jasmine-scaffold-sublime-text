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
			replacement = 'describe(\'' + line.lstrip(spacingType) + '\', function() {\n'
			indented = replacement.rjust(len(replacement) + currentWs, spacingType)
			scaffold.append(indented)
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

		settings = self.view.settings()
		spaceSize = settings.get('tab_size')
		tabsToSpaces = settings.get('translate_tabs_to_spaces')

		newLines = []

		# create an array of lines
		for line in file.splitlines():
			lines.append(line)

		# loop through each line
		for index, line in enumerate(lines):
			# number of whitespace at start of line
			currentWhitespace = self.countLineWhitespace(line, ' ')

			# the whitespace of the next line or -1 if the last line
			if index < len(lines)-1:
				nextWhitespace = self.countLineWhitespace(lines[index + 1], ' ')
			else:
				nextWhitespace = -1

			# the whitespace of the previous line or -1 if the first line
			if index == 0:
				previousWhitespace = -1
			else:
				previousWhitespace = self.countLineWhitespace(lines[index - 1], ' ')

			# if the previous line is more indented than the current one
			# we know that there is a new describe block and need to close
			# the previous describe block(s)
			if currentWhitespace < previousWhitespace:
				whitespaceDiff = (previousWhitespace - currentWhitespace)
				while whitespaceDiff > 0:
					whitespaceDiff -= spaceSize
					newLines.append('});'.rjust(3 + (whitespaceDiff + currentWhitespace) * spaceSize) + '\n\n')

			# if the current line's whitespace is larger than the next we have an
			# 'it should' block, else it's a 'describe' block
			if currentWhitespace > nextWhitespace:
				replacement = 'it(\'' + line.lstrip(' ' if tabsToSpaces else '\t') + '\', function() {\n\n'
				indented = replacement.rjust(len(replacement) + currentWhitespace*spaceSize)
				newLines.append(indented + '});'.rjust(3 + currentWhitespace*spaceSize) + '\n\n')
			else:
				replacement = 'describe(\'' + line.lstrip(' ' if tabsToSpaces else '\t') + '\', function() {\n\n'
				indented = replacement.rjust(len(replacement) + currentWhitespace*spaceSize)
				newLines.append(indented)

			# if we're at the end of the array we need to insert some '});''s depending
			# upon our current indentation
			if nextWhitespace == -1:
				a = currentWhitespace / spaceSize
				acpy = currentWhitespace
				while a > 0:
					a -= 1
					acpy -= spaceSize
					newLines.append('});'.rjust(3 + acpy) + '\n\n')

		# replace the whole view with the joined array we've just created
		self.view.replace(edit, region, ''.join(scaffolded))