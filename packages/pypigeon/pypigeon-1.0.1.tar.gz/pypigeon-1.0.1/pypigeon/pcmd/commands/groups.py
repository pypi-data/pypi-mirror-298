from pypigeon.pigeon_core.api.group import group_create_group
from pypigeon.pigeon_core.api.group import group_get_groups
from pypigeon.pigeon_core.api.group import group_update_group
from pypigeon.pigeon_core.models import GroupCreateGroupBody
from pypigeon.pigeon_core.models import GroupUpdateGroupBody
from pypigeon.pigeon_core.models import VisibilityLevel

from .base_commands import BaseCommands


class GroupsCommands(BaseCommands):
    """Operations on groups"""

    @BaseCommands._with_arg("name")
    @BaseCommands._with_arg("--public", action="store_true")
    def new(self) -> None:
        """Create a new group."""
        rv = group_create_group.sync(
            body=GroupCreateGroupBody(
                name=self.args.name,
                visibility_level=(
                    VisibilityLevel.PUBLIC
                    if self.args.public
                    else VisibilityLevel.UNLISTED
                ),
            ),
            client=self.core,
        )

        self._output(rv.to_dict())

    def list(self) -> None:
        """List all visible groups."""
        rv = group_get_groups.sync(client=self.core)

        self._output(rv.to_dict())

    @BaseCommands._with_arg("--name")
    @BaseCommands._with_arg("--make-public", action="store_true")
    @BaseCommands._with_arg("--make-unlisted", action="store_true")
    @BaseCommands._with_arg("group_id")
    def update(self) -> None:
        """Update a group."""
        update = GroupUpdateGroupBody()
        if self.args.name:
            update.name = self.args.name
        if self.args.make_public:
            update.visibility_level = VisibilityLevel.PUBLIC
        if self.args.make_unlisted:
            update.visibility_level = VisibilityLevel.UNLISTED
        group_update_group.sync(
            group_id=self.args.group_id, body=update, client=self.core
        )
