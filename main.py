import sublime
import sublime_plugin


class JasmineScaffoldCommand(sublime_plugin.TextCommand):

    DESCRIBE_LINE = 'describe(\'%s\', function() {\n\n'
    IT_LINE = 'it(\'%s\', function() {\n\n'

    def translatingTabsToSpaces(self):
        """Decide whether tabs are being translates to spaces or not."""
        return self.view.settings().get('translate_tabs_to_spaces')

    def spacingSetting(self):
        """Count the spacing being used."""
        return self.view.settings().get('tab_size')

    def countLineWhitespace(self, line, type):
        """Count the number of whitespace characters at the start of a line.

        Keyword arguments:
        self -- self
        line -- the line to count on
        type -- the type of spacing being used
        """
        return len(line) - len(line.lstrip(type))

    def getSelectedRegionStart(self, view, point):
        """Get the start of the region selected."""
        lineRegion = view.line(point)
        pos = lineRegion.a
        end = lineRegion.b
        while pos < end:
            ch = view.substr(pos)
            if ch != self.spacingSetting():
                break
            pos += 1
        return pos

    def buildScaffold(self, lines, spacingCount, spacingType, usingSpaces):
        """Build an array of lines to output to the file.

        Keyword arguments:
        self -- self
        lines -- the lines read from file or selection
        spacingCount -- the tab/space size being used
        spaingType -- space or tab character to input
        usingSpaces -- current user settings, spaces or tabs
        """
        scaffold = []

        for index, line in enumerate(lines):
            lineText = line.lstrip(spacingType)
            currentWhitespace = self.countLineWhitespace(line, spacingType)

            if index < len(lines) - 1:
                nextWhitespace = self.countLineWhitespace(
                    lines[index + 1], spacingType)
            else:
                nextWhitespace = self.countLineWhitespace(
                    lines[0], spacingType)

            descRepl = self.DESCRIBE_LINE % lineText
            indented = descRepl.rjust(
                len(descRepl) + currentWhitespace, spacingType)

            if currentWhitespace >= nextWhitespace:
                itRepl = self.IT_LINE % lineText
                decreasingWhitespace = currentWhitespace
                itReplIndent = itRepl.rjust(
                    len(itRepl) + currentWhitespace, spacingType)
                indented = []
                indented.append(itReplIndent + '});'.rjust(
                    3 + currentWhitespace, spacingType) + '\n\n')
                while decreasingWhitespace > nextWhitespace:
                    decreasingWhitespace -= spacingCount if usingSpaces else 1
                    closeBrackets = '});'.rjust(
                        3 + decreasingWhitespace, spacingType) + '\n\n'
                    indented.append(closeBrackets)

            scaffold.extend(indented)

        return scaffold

    def run(self, edit):
        lines = []
        fullFile = True

        # Create a region from the first sel to the last.
        if len(self.view.sel()[0]) == 0:
            # Full file.
            region = sublime.Region(0, self.view.size())
        else:
            # User selected part of file.
            fullFile = False
            for sel in self.view.sel():
                start = self.getSelectedRegionStart(
                    self.view, min(sel.a, sel.b))
                selectionEnd = self.view.line(max(sel.a, sel.b)).b
                region = sublime.Region(self.view.line(start).a, selectionEnd)

        file = self.view.substr(region)

        # Create an array of lines.
        for line in file.splitlines():
            lines.append(line)

        # Build the scaffolded tests, either for tab or space settings.
        if self.translatingTabsToSpaces():
            scaffolded = self.buildScaffold(
                lines, self.spacingSetting(), ' ', True)
        else:
            scaffolded = self.buildScaffold(
                lines, self.spacingSetting(), '\t', False)

        # Move cursor to end of selected text or file after transformation.
        self.view.sel().clear()
        self.view.sel().add(
            sublime.Region(self.view.size() if fullFile else selectionEnd))

        # Replace the whole view with the joined array we've just created.
        self.view.replace(edit, region, ''.join(scaffolded))
