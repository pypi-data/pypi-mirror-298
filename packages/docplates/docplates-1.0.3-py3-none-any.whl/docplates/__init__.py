#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2015-2024, AllWorldIT.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Main Docplates package.

This package is responsible for exporting pretty much everything that can be required to both use and customize Docplates.

"""

from .cmdline import DocplatesCommandLine
from .docplates import Docplates
from .exceptions import DocplatesError, DocplatesResourceNotFoundError, DocplatesUsageError
from .plugins.backends import DocplatesBackend
from .version import __version__

__all__ = [
    "Docplates",
    "DocplatesBackend",
    "DocplatesCommandLine",
    "DocplatesError",
    "DocplatesUsageError",
    "DocplatesResourceNotFoundError",
    "__version__",
]
