import subprocess

from . import left_menu_generator

def generate_left_menu(menu_file_name):
    left_menu_generator.generate_code(menu_file_name)

commands = {
    'left_menu': generate_left_menu
}

def generate(command_name, option='', **kwargs):
    if not command_name in commands:
        raise Exception(r'No command found: ' + command_name)
    commands[command_name](command_name)
    if option != None and option == 'update':
        print('Running webpack to rebuild frontend...')
        cmd = ['npm', 'run', 'dev']
        subprocess.call(cmd, shell=True)