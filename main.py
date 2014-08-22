import sublime
import sublime_plugin

class JazzCommand(sublime_plugin.TextCommand):

  def run(self, edit):

    lines = []
    newLines = []

    # create a region from the first sel to the last
    region = sublime.Region(0, self.view.size())
    file = self.view.substr(region)

    # create an array of lines
    for line in file.splitlines():
      lines.append(line)

    # loop through each line
    for index, line in enumerate(lines):
      # number of whitespace at start of line
      currentWhitespace = self.countWhitespace(line)

      # the whitespace of the next line or -1 if the last line
      if index < len(lines)-1:
        nextWhitespace = self.countWhitespace(lines[index + 1])
      else:
        nextWhitespace = -1

      # the whitespace of the previous line or -1 if the first line
      if index == 0:
        previousWhitespace = -1
      else:
        previousWhitespace = self.countWhitespace(lines[index - 1])

      # if the previous line is more indented than the current one
      # we know that there is a new describe block and need to close
      # the previous describe block(s)
      if currentWhitespace < previousWhitespace:
        whitespaceDiff = (previousWhitespace - currentWhitespace)
        while whitespaceDiff > 0:
          whitespaceDiff -= 2
          newLines.append('});'.rjust(3 + whitespaceDiff + currentWhitespace) + '\n\n')

      # if the current line's whitespace is larger than the next we have an
      # 'it should' block, else it's a 'describe' block
      if currentWhitespace > nextWhitespace:
        replacement = 'it(\'' + line.lstrip(' ') + '\', function() {\n\n'
        indented = replacement.rjust(len(replacement) + currentWhitespace)
        newLines.append(indented + '});'.rjust(3 + currentWhitespace) + '\n\n')
      else:
        replacement = 'describe(\'' + line.lstrip(' ') + '\', function() {\n\n'
        indented = replacement.rjust(len(replacement) + currentWhitespace)
        newLines.append(indented)

      # if we're at the of the array we need to insert some '});''s depending
      # upon our current indentation
      if nextWhitespace == -1:
        a = currentWhitespace / 2
        acpy = currentWhitespace
        while a > 0:
          a -= 1
          acpy -=2
          newLines.append('});'.rjust(3 + acpy) + '\n\n')

    # replace the whole view with the joined array we've just created
    self.view.replace(edit, region, ''.join(newLines))

  # yay, some modularity
  def countWhitespace(self, line):
    return len(line) - len(line.lstrip(' '))
