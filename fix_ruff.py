#!/usr/bin/env python3
"""Script to fix all remaining ruff errors systematically."""

import re


def fix_constants_file():
    """Fix constants file with proper docstrings."""
    file_path = "apps/common/constants.py"
    with open(file_path) as f:
        content = f.read()

    # Fix main docstring
    content = content.replace(
        '"""Constants for Wedding Planner API - Capstone MVP\n'
        'Keep it simple for graduation, expand after.\n"""',
        '"""Constants for Wedding Planner API - Capstone MVP.\n\n'
        'Keep it simple for graduation, expand after.\n"""',
    )

    # Add typing import
    content = content.replace(
        '"""Constants for Wedding Planner API - Capstone MVP.\n\n'
        'Keep it simple for graduation, expand after.\n"""\n\n',
        '"""Constants for Wedding Planner API - Capstone MVP.\n\n'
        'Keep it simple for graduation, expand after.\n"""\n\n'
        "from typing import ClassVar\n\n",
    )

    # Add class docstrings and ClassVar annotations
    classes = [
        ("class TaskAssignment:", '    """Task assignment choices for wedding planning."""'),
        ("class RSVPStatus:", '    """RSVP status choices for guest management."""'),
        ("class VendorCategory:", '    """Vendor category choices for wedding services."""'),
        ("class TeamRole:", '    """Team role choices for wedding party members."""'),
        ("class Messages:", '    """Standard API response messages."""'),
    ]

    for class_line, docstring in classes:
        content = content.replace(class_line, f"{class_line}\n{docstring}")

    # Add ClassVar to CHOICES
    content = re.sub(r"    CHOICES = \[", "    CHOICES: ClassVar = [", content)

    with open(file_path, "w") as f:
        f.write(content)


def fix_serializer_file(file_path, app_name):
    """Fix serializer files with ClassVar and docstrings."""
    with open(file_path) as f:
        content = f.read()

    # Add typing import if not present
    if "from typing import ClassVar" not in content:
        content = content.replace(
            "from rest_framework import serializers",
            "from typing import ClassVar\n\nfrom rest_framework import serializers",
        )

    # Add ClassVar to fields
    content = re.sub(r"        fields = \[", "        fields: ClassVar = [", content)
    content = re.sub(
        r"        read_only_fields = \[", "        read_only_fields: ClassVar = [", content
    )

    # Add Meta class docstrings
    content = re.sub(
        r"    class Meta:\n        model",
        (
            '    class Meta:\n        """Meta configuration for serializer."""\n'
            "        \n        model"
        ),
        content,
    )

    # Add method docstrings for missing ones
    if "def validate_" in content:
        # Add docstrings to validation methods that don't have them
        content = re.sub(
            r"    def validate_([a-zA-Z_]+)\(self, value\):\n        valid_choices",
            r"    def validate_\1(self, value):\n"
            r'        """Validate \1 field."""\n        valid_choices',
            content,
        )

    create_method_start = content.find("def create(self, validated_data):")
    if (
        create_method_start != -1
        and '"""' not in content[create_method_start : create_method_start + 100]
    ):
        content = content.replace(
            "def create(self, validated_data):",
            "def create(self, validated_data):\n"
            '        """Create instance with auto-assignment."""',
        )

    with open(file_path, "w") as f:
        f.write(content)


def fix_validators_file():
    """Fix validators file docstring."""
    file_path = "apps/common/validators/base.py"
    with open(file_path) as f:
        content = f.read()

    content = content.replace(
        '"""Basic validators for Wedding Planner API - Capstone MVP\n'
        'Keep it simple for graduation.\n"""',
        '"""Basic validators for Wedding Planner API - Capstone MVP.\n\n'
        'Keep it simple for graduation.\n"""',
    )

    with open(file_path, "w") as f:
        f.write(content)


# Run fixes
fix_constants_file()
fix_validators_file()

serializer_files = [
    ("apps/profiles/serializers.py", "profiles"),
    ("apps/tasks/serializers.py", "tasks"),
    ("apps/guests/serializers.py", "guests"),
    ("apps/vendors/serializers.py", "vendors"),
]

for file_path, app_name in serializer_files:
    fix_serializer_file(file_path, app_name)
