"""
Panther Core is a Python library for Panther Detections.
Copyright (C) 2020 Panther Labs Inc

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import contextlib
from types import TracebackType
from typing import Any, List, Optional, Type
from unittest.mock import MagicMock, patch

no_op_logger = MagicMock()


class ExecutionContextManager:
    """
    ExecutionContextManager is responsible for setting various constraints at detection execution time

    The constraints imposed are:
    1. Preventing writing to stdout and stderr
    2. Patching any calls to the logging package
    """

    def __init__(self, disable_output: bool, patch_logger: bool = False) -> None:
        self.contexts: List[Any] = []
        if disable_output:
            self.contexts.extend(
                [
                    contextlib.redirect_stdout(None),
                    contextlib.redirect_stderr(None),
                ]
            )
        if patch_logger:
            self.contexts.append(patch("logging", no_op_logger))

        self.exit_stack = contextlib.ExitStack()

    def __enter__(self) -> "ExecutionContextManager":
        # Enter all the provided context managers
        for context in self.contexts:
            self.exit_stack.enter_context(context)
        return self

    def __exit__(
        self,
        _exc_type: Optional[Type[BaseException]],
        _exc_val: Optional[BaseException],
        _exc_tb: Optional[TracebackType],
    ) -> None:
        self.exit_stack.__exit__(_exc_type, _exc_val, _exc_tb)
