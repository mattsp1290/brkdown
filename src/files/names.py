import randomname
from ..sqlite.db import DB
import click
import os
import re
from ..config.config import Config

def get_next_name(target_name, current_iteration=0):
    next_name = f"{target_name}_{current_iteration}"
    rows = DB().execute(f"SELECT * FROM file_names WHERE name='{file_path}'").fetchall()
    if rows:
        click.echo(f"found file with name {next_name}")
        get_next_name(target_name, current_iteration=current_iteration+1)
    command = (f"INSERT INTO file_names VALUES ('{next_name}')")
    DB().execute(command)
    DB().commit()
    return next_name
    

def get_brk_name(file_path):
    # cursor = connection.cursor()
    # cursor.execute("CREATE TABLE file_aliases (original_name TEXT, new_name TEXT)")
    # generate name using all categories
    original_name_rows = DB().execute(f"SELECT original_name, new_name FROM file_aliases WHERE original_name='{file_path}'").fetchall()
    if original_name_rows:
        return original_name_rows[0][1]
    
    # name = randomname.get_name()
    name = brk_path_name(file_path)
    command = (f"INSERT INTO file_aliases VALUES ('{file_path}', '{name}')")
    DB().execute(command)
    DB().commit()
    click.echo(command)
    return name

def brk_path_name(file_path):
    db_path = get_db_path(file_path)
    original_name_rows = DB().execute(f"SELECT * FROM path_aliases WHERE original_name='{db_path}'").fetchall()
    if original_name_rows:
        click.echo(original_name_rows)
        return original_name_rows[0][1]
    
    current_directory = Config().get_value("CURRENT_DIRECTORY")
    base_path = os.path.basename(current_directory)
    click.echo(f"base path {base_path} from {current_directory}")
    words = re.findall(r"[\w']+", base_path)
    click.echo(words)

    initialism = []

    initialism_length = 8

    initials_included = 0
    for i in range(initialism_length):
        if i < len(words) and initials_included < 4:
            initialism.append(words[i][0].upper())
            initials_included += 1
        else:
            initialism.append(randomname.get_name()[0].upper())

    name = "".join(initialism)  
    command = (f"INSERT INTO path_aliases VALUES ('{db_path}', '{name}')")
    click.echo(f"insert: {command}")
    DB().execute(command)
    DB().commit()
    return name
    

def get_db_path(file_path):
    words = re.findall(r"[\w']+", file_path)
    return "".join(words)