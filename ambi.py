import os
import pickle

db = {
    'username': None,
    'subjects': [],
    'backlog': [],
    'today': [],
    'done': []
}

def table_output(cols):
    top = 0
    for col in cols:
        if len(col['data']) > 0:
            top += len(max(col['data'], key=len)) + 3
    if top != 0 and sum(len(col['data']) for col in cols) > 0:
        print('+' + '-'*(top-2) + '+')

    for row in range(-1, max(len(col['data']) for col in cols)):
        for col in range(0, len(cols)):
            if row == -1 and len(cols[col]['data']) > 0:
                print('| ' + cols[col]['title'], end='')
                print(' '*(max(len(item) for item in cols[col]['data']) - len(cols[col]['title'])) + '|', end='')
            elif row < len(cols[col]['data']) and row != -1:
                print('| ' + cols[col]['data'][row] + ' '*(max(len(entry) for entry in cols[col]['data']) - len(cols[col]['data'][row])) + '|', end='')
            elif len(cols[col]['data']) > 0:
                print('| ' + ' '*(max(len(entry) for entry in cols[col]['data'])) + '|', end='')

        if row == -1 and sum(len(col['data']) for col in cols) > 0:
            print('\n+' + '-'*(top-2) + '+')
        else:
            print('')

    if sum(len(col['data']) for col in cols) > 0:
        print('+' + '-'*(top-2) + '+')

def menu():
    if db['username'] is None:
        setup()
    print(f"Welcome {db['username']}! Enter h for help.")
    while True:
        save()

        cols = []
        cols.append({'title': 'backlog', 'data': bundle('backlog')})
        cols.append({'title': 'today', 'data': bundle('today')})
        cols.append({'title': 'done (last 10)', 'data': bundle('done')})
        table_output(cols)
        cmd = input('Enter command: ')
        commands = {
            'h': help,
            'c': clear_terminal,
            'n': backlog_add,
            'r': backlog_remove,
            'a': today_add,
            'd': today_done,
            's': subjects_list,
            'sa': subjects_add,
            'p': purge
        }
        if cmd == 'e':
            break
        elif cmd not in commands:
            print('Command not found, try h for help')
        else:
            commands[cmd]()

    print('Goodbye!')

def help():
    print('current commands:')
    help_str = '''
    h: displays this
    c: clears terminal
    e: exits application
    n: adds a task to the backlog
    r: removes a task from the backlog
    a: adds a task from the backlog to today
    d: sets a task for today as 'done'
    s: lists subjects
    sa: adds a subject
    p: purges database
    '''
    print(help_str)

def clear_terminal():
    os.system('clear')

def bundle(collection):
    items = []
    count = 1
    if collection != 'done':
        db[collection].sort(key=lambda x: x['priority'], reverse=True)
    for task in db[collection]:
        items.append(f"{count}. {(task['priority']*'*')[0:3] + (3 - task['priority'])*' '} | {task['subject']} | {task['type']} | {task['desc']} ")
        count += 1
        if collection == 'done' and count >= 10:
            break

    return items

def backlog_add():
    priority = int(input('Priority? (1-3): '))

    if len(db['subjects']) == 0:
        print('No subjects found. Add one using the command sa')
        return
    sub_list = ''
    for i in range(0, len(db['subjects'])):
        sub_list += f"[{i+1}] {db['subjects'][i]}, "
    sub_list = sub_list[:-2]
    subject = db['subjects'][int(input(f"Subject? ({sub_list}): "))-1]

    types = ['study', 'revision', 'homework', 'exam']
    task_type_input = int(input('Type? ([1] study, [2] revision, [3] homework, [4] exam): '))
    task_type = types[task_type_input-1] +  (8-len(types[task_type_input-1]))*' '

    desc = input('Concise description? (subject to terminal width): ')

    db['backlog'].append(
        {
            'priority': priority,
            'subject': subject,
            'type': task_type,
            'desc': desc
        }
    )

def backlog_remove():
    num = int(input('Number to remove?: '))
    del db['backlog'][num-1]

def today_add():
    num = int(input('Number to move from backlog to today?: '))
    db['today'].append(db['backlog'][num-1])
    del db['backlog'][num-1]

def today_done():
    num = int(input('Todays task num completed?: '))
    db['done'].insert(0, db['today'][num-1])
    del db['today'][num-1]

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

DB_FILE_NAME = 'database.pickle'

def load():
    try:
        global db
        db = pickle.load(open(DB_FILE_NAME, 'rb'))
    except FileNotFoundError:

        save()

def save():
    with open(DB_FILE_NAME, 'wb') as file:
        pickle.dump(db, file)

def purge():
    response = input('This will purge the whole database. Continue? (y/n): ')
    if response == 'y':
        global db
        db = {
            'username': None,
            'subjects': [],
            'backlog': [],
            'today': [],
            'done': []
        }
        save()
        setup()
    else:
        print('Aborted, returning to menu.')

if __name__ == '__main__':
    load()
    menu()