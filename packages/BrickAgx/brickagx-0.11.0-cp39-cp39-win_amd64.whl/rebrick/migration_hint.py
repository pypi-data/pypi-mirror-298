"""
Migration hint for use by cmdline tools
"""
from rebrick import check_if_migrate_hint_is_justified, __version__

class Ansi: # pylint: disable=too-few-public-methods # This is basically an enum, but we do not want to use Enum
    WARNING = '\033[93m'
    ENDC = '\033[0m'

def check_migration_hint(brickfile, errors):
    old_version = check_if_migrate_hint_is_justified(__version__, errors)
    if old_version:
        print(f"{Ansi.WARNING}Dependency errors might be due to upgrade. If so, try running: "
                f"brickmigrate --from-version {old_version} {brickfile}{Ansi.ENDC}")
