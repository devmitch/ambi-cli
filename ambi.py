db = {
    'username': None,
    'subjects': [],
    'backlog': [],
    'today': {},
    'done': []
}

def menu():
    if db['username'] is None:
        setup()
    print(f"Welcome {db['username']}!")
    print('Enter h for help')
    while True:
        cmd = input('Enter command: ')
        commands = {
            'h': help,
            'b': backlog_display,
            #'t': today_display,
            'n': backlog_add,
            'r': backlog_remove,
            #'a': today_add,
            #'d': today_done,
            's': subjects_list,
            'sa': subjects_add
        }
        if cmd == 'e':
            break
        commands[cmd]()

    print('Goodbye!')

def help():
    print('current commands:')
    help_str = '''
    h: displays this
    b: lists all tasks in backlog
    t: lists all tasks for today
    n: adds a task to the backlog
    r: removes a task from the backlog
    a: adds a task from the backlog to today
    d: sets a task for today as 'done'
    s: lists subjects
    sa: adds a subject
    '''
    print(help_str)

def backlog_display():
    count = 1
    for task in db['backlog']:
        print(f"{count}. {task['priority']} | {task['subject']} | {task['type']} | {task['desc']}")
        count += 1

def backlog_add():
    priority = input('Priority? (l, m, h): ')
    subject = input(f"Subject? ({db['subjects']}): ")
    task_type = input('Type? (study, revision, homework): ')
    desc = input('Description?: ')
    db['backlog'].append(
        {
            'priority': priority,
            'subject': subject,
            'type': task_type,
            'desc': desc
        }
    )
    print('Added new task to backlog! Returning to menu...')

def backlog_remove():
    backlog_display()
    num = int(input('Number to remove?: '))
    del db['backlog'][num-1]
    print('Removed task from backlog! Returning to menu...')

def subjects_list():
    if not db['subjects']:
        print('No subjects to display. Add one with command sa')
    for sub in db['subjects']:
        print(sub)

def subjects_add():
    sub = input('Subject to add?: ')
    db['subjects'].append(sub)

def setup():
    db['username'] = ('Welcome to ambi, what is your name? ')

if __name__ == '__main__':
    menu()