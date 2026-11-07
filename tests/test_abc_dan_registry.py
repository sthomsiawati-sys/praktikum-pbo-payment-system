import pytest

from core.base import PaymentMethod
from core.registry import buat_metode, daftar_plugin
from plugins import muat_semua_plugin


def test_abc_tidak_bisa_diinstansiasi():
    with pytest.raises(TypeError):
        PaymentMethod("uji")  # type: ignore[abstract]


def test_subclass_tidak_lengkap_tidak_bisa_diinstansiasi():
    class Setengah(PaymentMethod):
        def validasi(self, jumlah: float) -> bool:
            return True

    with pytest.raises(TypeError):
        Setengah("uji")  # type: ignore[abstract]


def test_plugin_tak_dikenal_memunculkan_keyerror():
    muat_semua_plugin()
    with pytest.raises(KeyError):
        buat_metode("tidak-ada")


def test_plugin_bawaan_terdaftar():
    muat_semua_plugin()
    assert {"transfer", "ewallet", "qris", "va"} <= set(daftar_plugin())