#   -------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------
"""Python Package Template"""
from __future__ import annotations
from .rosetta_finder import RosettaBinary, RosettaFinder, main
from .rosetta import Rosetta

__all__ = ["RosettaFinder", "RosettaBinary", "main", "Rosetta"]

__version__ = "0.0.5""-rc54-post1"
