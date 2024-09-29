from busy.error import BusyError

from busy.integration import Integration


class GitLabIntegration(Integration):

    QUEUE = 'tasks'

    def sync(self, command):
        app = command.app
        dones = app.storage.get_collection(self.QUEUE, 'done')
        todos = app.storage.get_collection(self.QUEUE, 'todo')
        plans = app.storage.get_collection(self.QUEUE, 'plan')
        issue = self.issue(todos[0])
        alltodos = [t.base for t in todos[1:] if self.issue(t) == issue]
        utodos = []
        [utodos.append(x) for x in alltodos if x not in utodos]
        allplans = [t.base for t in plans if self.issue(t) == issue]
        uplans = []
        [uplans.append(x) for x in allplans if x not in (utodos + uplans)]
        alldones = [t.base for t in dones if self.issue(t) == issue]
        udones = []
        [udones.append(x)
         for x in alldones if x not in (utodos + uplans + udones)]
        fmtdones = [f"- [x] {d}\n" for d in udones]
        fmttodos = [f"- [ ] {t}\n" for t in utodos]
        fmtplans = [f"- [ ] {p}\n" for p in uplans]
        return "".join(fmtdones + fmttodos + fmtplans)

    def get(self, command):
        """Right now just assuming we want an issue"""
        if command.selection:
            item = command.selected_items[0]
            return self.issue(item)

    @staticmethod
    def issue(item):
        val = item.data_value('i')
        if val and val.isdigit():
            return val

    # def first_item(self, app): """The current task underway. Please give this
    #     function a new name.""" todos =
    #     app.storage.get_collection(self.QUEUE, 'todo') return todos[0]

    # def first_item_configured_tag(self, app):
    #     """The tag that matters - one from the config that's in the current
    #     task"""
    #     my_tags = self.first_item(app).tags
    #     config = app.config.get('busy-integrations-gitlab-tags')
    #     configured = config.split(' ') if config else []
    #     tag = next((t for t in configured if t in my_tags), None)
    #     return tag


Main = GitLabIntegration
