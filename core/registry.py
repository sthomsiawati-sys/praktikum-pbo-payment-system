from collections.abc import Callable
from typing import Any, TypeVar

from core.base import PaymentMethod

T = TypeVar("T", bound=PaymentMethod)

_REGISTRY: dict[str, type[PaymentMethod]] = {}


def register_plugin(kode: str) -> Callable[[type[T]], type[T]]:
    """Dekorator: daftarkan kelas metode pembayaran sebagai plugin."""

    def dekorator(kelas: type[T]) -> type[T]:
        if not issubclass(kelas, PaymentMethod):
            raise TypeError(f"{kelas.__name__} harus turunan PaymentMethod")
        _REGISTRY[kode] = kelas
        return kelas

    return dekorator


def daftar_plugin() -> list[str]:
    return sorted(_REGISTRY)


def buat_metode(kode: str, **kwargs: Any) -> PaymentMethod:
    if kode not in _REGISTRY:
        raise KeyError(
            f"Plugin {kode!r} tidak ditemukan. Tersedia: {daftar_plugin()}"
        )
    return _REGISTRY[kode](**kwargs)