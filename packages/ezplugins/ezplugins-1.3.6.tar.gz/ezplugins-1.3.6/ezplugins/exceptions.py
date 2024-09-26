#
# SPDX-License-Identifier: MIT
#
# Copyright (C) 2019-2024, AllWorldIT.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""EZPlugins exceptions."""

__all__ = [
    "EZPluginError",
    "EZPluginMethodNotFoundError",
]


class EZPluginError(Exception):
    """EZPlugin related exception base class."""


class EZPluginMethodNotFoundError(EZPluginError):
    """
    Exception raised when a plugin method or plugin is not found during a :meth:`~ezplugins.manager.EZPluginManager.methods` call.

    Parameters
    ----------
    method_name : :class:`str` | None
        Method name.

    plugin_name : :class:`str` | None
        Plugin name.

    """

    _plugin_name: str | None
    _method_name: str | None

    def __init__(self, method_name: str | None, plugin_name: str | None):
        """
        Exception raised when a plugin method or plugin is not found during a \
        :meth:`~ezplugins.manager.EZPluginManager.methods` call.

        Parameters
        ----------
        method_name : :class:`str` | None
            Method name.

        plugin_name : :class:`str` | None
            Plugin name.

        """

        super().__init__("No EZPlugin method(s) found")

        self._plugin_name = plugin_name
        self._method_name = method_name

    @property
    def plugin_name(self) -> str | None:
        """Plugin name if one is available."""
        return self._plugin_name

    @property
    def method_name(self) -> str | None:
        """Name of the method if one is available."""
        return self._method_name
