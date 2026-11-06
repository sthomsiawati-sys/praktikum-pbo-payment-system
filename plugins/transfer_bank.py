from core.base import PaymentMethod
from core.registry import register_plugin
from core.utils import buat_id
 

@register_plugin("transfer")
class TransferBank(PaymentMethod):
    def __init__(self, saldo: float = 0, bank: str = "BCA"):
        super().__init__(f"Transfer {bank}")
        self.saldo = saldo
 
    def validasi(self, jumlah: float) -> bool:
        return self.saldo >= jumlah
 
    def bayar(self, jumlah: float) -> str:
        self.saldo -= jumlah
        return buat_id("TRF")

    def biaya_admin(self, jumlah: float) -> float:
        return 2_500
