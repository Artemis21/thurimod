"""Run the Thuri Mod bot."""
from migration import upgrade_db

from . import database  # noqa: F401
from .bot import mainloop

if __name__ == "__main__":
    upgrade_db()
    mainloop()
