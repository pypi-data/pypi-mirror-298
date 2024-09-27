from pypigeon.pigeon_core.api.admin import admin_list_admins

from .base_commands import BaseCommands
from .config import ConfigCommands


class AdminCommands(BaseCommands):
    """Administrative operations"""

    config = ConfigCommands

    def list_admins(self) -> None:
        """List system admins and privileges."""
        rv = admin_list_admins.sync(client=self.core)

        self._output(
            [
                {"subject_id": r.subject_id, "operations": ",".join(r.operations)}
                for r in rv.grants
            ],
            preferred_type="table",
        )

        if rv.operations:
            print()
            print("Operations:")
            for op in rv.operations:
                print("-", op)
