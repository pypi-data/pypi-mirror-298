from __future__ import annotations

import typing as t

from traitlets import TraitType, Undefined, Union


class Attribute(Union):
    """An application attribute that is automatically synced with the widget."""

    info_text = "an attribute"

    @property
    def attribute_name(self) -> str:
        """The html attribute name.

        Raises:
            AttributeError: If an attribute name has not been set.
        """
        if self.metadata["attribute_name"]:
            return self.metadata["attribute_name"]
        elif self.name:
            return self.name.replace("_", "-").removeprefix("-")
        else:
            raise AttributeError("Cannot determine an attribute_name")

    @property
    def required(self) -> bool:
        """Whether the attribute must have a value."""
        return self.metadata["required"]

    @property
    def _definition(self):
        return {"name": self.attribute_name, "key": self.name}

    def __init__(
        self,
        trait: TraitType,
        default_value: t.Any = Undefined,
        attribute_name: str | None = None,
        required=False,
        allow_none=False,
        read_only: bool | None = None,
        help: str | None = None,
    ) -> None:
        """Declares a new attribute.

        Args:
            trait (TraitType): Trait used to validate attribute values.
            default_value (t.Any, optional): Default value for the attribute.
            attribute_name (str | None, optional): Html attribute name, inferred if not provided.
            required (bool, optional): Whether a value is required for the attribute. Defaults to False.
            allow_none (bool, optional): Whether to allow None values. Defaults to False.
            read_only (bool | None, optional): Whether the attribute is read only. Defaults to None.
            help (str | None, optional): Attribute help documentation. Defaults to None.
        """
        super().__init__(
            trait.trait_types if isinstance(trait, Union) else [trait],
            default_value=default_value,
            allow_none=allow_none,
            read_only=read_only,
            help=help,
        )
        self.info_text = f"an attribute of {trait.info_text}"
        self.tag(
            type="attribute",
            attribute_name=attribute_name,
            required=required,
            sync=True,
        )
