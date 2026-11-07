from collections.abc import Callable
from datetime import datetime, timedelta

from core.base import PaymentMethod
from core.registry import register_plugin
from core.utils import buat_id


@register_plugin("va")
class VirtualAccount(PaymentMethod):
    """Virtual Account: tagihan dibuat dulu (status 'menunggu'), lalu
    dibayar sebelum batas waktu. Lewat batas waktu -> 'kedaluwarsa'."""

    BIAYA_ADMIN = 4_000

    def __init__(
        self,
        tagihan: float = 0,
        bank: str = "BNI",
        batas_jam: int = 24,
        sekarang: Callable[[], datetime] = datetime.now,
    ):
        super().__init__(f"Virtual Account {bank}")
        self.tagihan = tagihan
        self._sekarang = sekarang  # bisa diganti saat pengujian
        self.batas_waktu = sekarang() + timedelta(hours=batas_jam)
        self._lunas = False

    @property
    def status(self) -> str:
        if self._lunas:
            return "lunas"
        if self._sekarang() > self.batas_waktu:
            return "kedaluwarsa"
        return "menunggu"

    def biaya_admin(self, jumlah: float) -> float:
        return self.BIAYA_ADMIN

    def validasi(self, jumlah: float) -> bool:
        # 'jumlah' di sini adalah total (tagihan + biaya admin)
        return (
            self.status == "menunggu"
            and jumlah == self.tagihan + self.BIAYA_ADMIN
        )

    def bayar(self, jumlah: float) -> str:
        self._lunas = True
        return buat_id("VAC")