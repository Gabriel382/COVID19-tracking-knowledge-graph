from os.path import exists

def print_file_in_log(file_name, line):
    contents = []
    if exists(file_name):
        f = open(file_name, 'r+')
        contents = [x[:-1] for x in f.readlines()]
    with open(file_name, 'a+') as f:
        if line not in contents:
            f.write(line + '\n')

def is_log_written(file_name, line):
    if exists(file_name):
        with open(file_name, 'r+') as f:
            contents = [x[:-1] for x in f.readlines()]
            if line in contents:
                return True
            else:
                return False
    return False