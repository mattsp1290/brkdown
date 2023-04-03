from .db import DB
import click

MIGRATIONS = [
    ("file_aliases", "CREATE TABLE file_aliases (original_name TEXT, new_name TEXT)"),
    ("path_aliases", "CREATE TABLE path_aliases (original_name TEXT, new_name TEXT)"),
    ("file_names", "CREATE TABLE file_names (name TEXT)")
]

def run_migration(table_name, create_command):
    try:    
        DB().execute(create_command)
    except Exception as e:
        click.echo(f"Exception running migration for table {table_name}")
        click.echo(e)

def run_migrations():
    for table_name, create_command in MIGRATIONS:
        run_migration(table_name, create_command)