from .task_item import TaskItem
from datetime import datetime
from pympmyansi import pymp


def list_tasks(listarg: str, tasks: list[TaskItem]) -> None:
    if len(tasks) == 0:
        print("You have no todos!")
        return
    if listarg == 'all':
        for t in tasks:
            print(t)
    else:
        match = False
        for t in tasks:
            if t.status == listarg:
                print(t)
                if not match:
                    match = True
        if not match:
            print(f'nothing in {listarg}!')


def add_task(name: str, tasks: list, desc: str = '') -> None:
    date = datetime.now()
    newdate = str(date.month) + "/" + str(date.day) + "/" + str(date.year)
    if len(tasks) == 0:
        newid = 0
    else:
        newid = tasks[-1].id + 1
    t = TaskItem(id=newid, name=name, desc=desc,
                 status="todo", start_date=newdate)
    tasks.append(t)
    print("added", t)


def del_task_by_id(taskids: list[int], tasks: list[TaskItem]) -> list:
    newlist = []
    newid = 0
    for t in tasks:
        if t.id not in taskids:
            t.id = newid
            newlist.append(t)
            newid += 1
        else:
            print(pymp("deleted", 'underline'), t)
    return newlist


def del_task_by_grp(taskset: str, tasks: list[TaskItem]) -> list:
    newlist = []
    if taskset == 'all':
        pass
    else:
        for t in tasks:
            if t.status != taskset:
                newlist.append(t)
    print(pymp(pymp('deleted', 'underline'), 'fg_red'), 'all in', taskset)
    return newlist


def set_task(taskids: list[int], group: str, tasks: list[TaskItem]) -> None:
    color = ''
    match group:
        case 'todo':
            color = 'fg_red'
        case 'doing':
            color = 'fg_yellow'
        case 'done':
            color = 'fg_green'
    for t in tasks:
        if t.id in taskids:
            t.status = group
            print(f"marked {t.name} as", pymp(group, color))


# TODO let you update tasks
