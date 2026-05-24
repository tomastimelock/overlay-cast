from __future__ import annotations


class OverlayCastError(Exception):
    pass


class StyleNotFoundError(OverlayCastError):
    def __init__(self, slug: str) -> None:
        super().__init__(f"Style not found: {slug!r}")
        self.slug = slug


class CatalogLoadError(OverlayCastError):
    pass


class RenderError(OverlayCastError):
    pass


class ConfigError(OverlayCastError):
    pass
