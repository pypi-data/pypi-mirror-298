from __future__ import annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING
from functools import partial as _partial

from exceptionman import _traceback

if _TYPE_CHECKING:
    from rich.console import Console
    from mdit.document import Document


class ReporterException(Exception):
    """Base exception class with HTML reporting capabilities."""

    def __init__(
        self,
        report: Document,
        sphinx_config: dict | None = None,
        sphinx_args: dict | None = None,
        console: Console | None = None,
    ):
        import mdit as _mdit

        # console_renderable =
        # console = _Console()
        # with console.capture() as capture:
        #     console.print(console_renderable)
        # console_text = capture.get()
        sphinx_args = {
            "status": None,
            "warning": None,
        } | (sphinx_args or {})
        target_config = _mdit.target.sphinx()
        target_config.renderer = _partial(
            _mdit.render.sphinx,
            config=sphinx_config,
            **sphinx_args
        )
        report.default_output_target = target_config
        self.report = report
        super().__init__()
        if not _traceback.USER_INSTALLED:
            _traceback.install(temporary=True)
        return

    def __rich__(self) -> str:
        return self.report.render(target="console", filters="console")
