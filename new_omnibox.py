import sublime
import sublime_plugin


class OpenCmdCommand(sublime_plugin.WindowCommand):
    def run(self):
        sublime.status_message("hello")
        v = self.window.new_file()
        v.set_name("Sublime CMD")
        v.set_scratch(True)
        v.settings().set("is_cmd", True)
        edit = v.begin_edit()
        v.insert(edit, 0, '=' * 80)
        v.insert(edit, 0, '\n')
        v.end_edit(edit)
        v.sel().clear()
        v.sel().add(sublime.Region(0, 0))


class ExecCmdCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        return self.view.settings().get('is_cmd')

    def run(self, edit):
        cmd_line = self.view.substr(self.view.line(self.view.sel()[0]))
        cmd_line = cmd_line[4:]
        print "CMD Line:", cmd_line
 
        out = ''
        if cmd_line.startswith('run:w '):
            cmd_line = cmd_line[len('run:w '):]
            head, _, tail = cmd_line.partition(' ')
            print "XXX", cmd_line.partition(' ')
            if head and tail:
                print "Running:", head, "Args:", tail
                sublime.active_window().run_command(str(head), eval(tail))
            elif head:
                sublime.active_window().run_command(str(head))
                print "Running:", head
            else:
                out = "Error: No command found."
        
        elif cmd_line.startswith('cls'):
            self.view.replace(edit, sublime.Region(0, self.view.size()), '')

        if out: out = "\n" + out
        self.view.replace(edit, self.view.sel()[0], out + "\nSu] ")

        end = self.view.sel()[-1].end()
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(end, end))
