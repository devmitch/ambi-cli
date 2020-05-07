db = {
    'username': None,
    'subjects': [],
    'backlog': [],
    'today': [],
    'done': []
}

def table_output():
    cols = []
    cols.append({'title': 'backlog', 'data': backlog_bundle()})
    cols.append({'title': 'today', 'data': today_bundle()})
    top = 0
    for col in cols:
        if len(col['data']) > 0:
            top += len(max(col['data'], key=len)) + 3
    if top != 0:
        print('+' + '-'*(top-2) + '+')
    #print(cols)
    for row in range(-1, max(len(col['data']) for col in cols)):
        for col in range(0, len(cols)):
            if row == -1 and len(cols[col]['data']) > 0:
                print('| ' + cols[col]['title'], end='')
                print(' '*(max(len(item) for item in cols[col]['data']) - len(cols[col]['title'])) + '|', end='')
            elif row < len(cols[col]['data']) and row != -1:
                print('| ' + cols[col]['data'][row] + ' '*(max(len(entry) for entry in cols[col]['data']) - len(cols[col]['data'][row])) + '|', end='')
        if row == -1:
            print('\n+' + '-'*(top-2) + '+')
        else:
            print('')
    print('+' + '-'*(top-2) + '+')


    '''
    for col in cols:
        if len(col['data']) > 0:
            m_width = len(max(col['data'], key=len))
            print('+' + '-'*(m_width) + '+')
            for item in col['data']:
                print(f"|{item}{' '*(m_width-len(item))}|")
            print('+' + '-'*(m_width) + '+')
    '''
def menu():
    if db['username'] is None:
        setup()
    print(f"Welcome {db['username']}! Enter h for help.")
    while True:
        table_output()
        cmd = input('Enter command: ')
        commands = {
            'h': help,
            #'b': backlog_display,
            #'t': today_display,
            'n': backlog_add,
            'r': backlog_remove,
            'a': today_add,
            'd': today_done,
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
    e: exits application
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

def backlog_bundle():
    '''
    Bundle up backlog entries as a list of strings to be displayed in table
    '''
    items = []
    count = 1
    for task in db['backlog']:
        items.append(f"{count}. {task['priority']} | {task['subject']} | {task['type']} | {task['desc']}")
        count += 1
    return items

def backlog_add():
    priority = input('Priority? (*, **, ***): ')
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
    num = int(input('Number to remove?: '))
    del db['backlog'][num-1]
    print('Removed task from backlog! Returning to menu...')

def today_add():
    num = int(input('Number to move from backlog to today?: '))
    db['today'].append(db['backlog'][num-1])
    del db['backlog'][num-1]
    print('Moved task to today! Returning to menu...')

def today_done():
    num = int(input('Todays task num completed?: '))
    del db['today'][num-1]
    print('Completed task for today! Returning to menu...')

def today_bundle():
    '''
    Bundle up today entries as a list of strings to be displayed in table
    '''
    items = []
    count = 1
    for task in db['today']:
        items.append(f"{count}. {task['priority']} | {task['subject']} | {task['type']} | {task['desc']}")
        count += 1
    return items

def subjects_list():
    if not db['subjects']:
        print('No subjects to display. Add one with command sa')
    for sub in db['subjects']:
        print(sub)

def subjects_add():
    sub = input('Subject to add?: ')
    db['subjects'].append(sub)

def setup():
    db['username'] = input('Welcome to ambi, what is your name? ')

if __name__ == '__main__':
    menu()