from dataclasses import dataclass
from pympmyansi import pymp


@dataclass
class TaskItem:
    """Represents a todo item."""
    id: int
    name: str
    desc: str
    status: str
    start_date: str

    def __repr__(self):
        newname = self.name
        newstatus = self.status
        newdesc = pymp(self.desc, 'fg_dark_gray')
        newdate = pymp(self.start_date, 'fg_purple')
        if self.status == 'todo':
            newname = pymp(newname, 'fg_red')
            newstatus = pymp(newstatus, 'fg_red')
        elif self.status == 'doing':
            newname = pymp(newname, 'fg_yellow')
            newstatus = pymp(newstatus, 'fg_yellow')
        elif self.status == 'done':
            newname = pymp(newname, 'fg_green')
            newstatus = pymp(newstatus, 'fg_green')
        return f"{str(self.id)}. {newname} | {newdesc}\n" + \
            f"{newstatus}   added: {newdate}"
