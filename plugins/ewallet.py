from core.base import PaymentMethod
from core.registry import register_plugin
from core.utils import buat_id
 
 
@register_plugin("ewallet")
class EWallet(PaymentMethod):
    BATAS_TRANSAKSI = 2_000_000
 
    def __init__(self, saldo: float = 0, provider: str = "GoPay"):
        super().__init__(f"E-Wallet {provider}")
        self.saldo = saldo
 
    def validasi(self, jumlah: float) -> bool:
        return jumlah <= self.BATAS_TRANSAKSI and self.saldo >= jumlah
 
    def bayar(self, jumlah: float) -> str:
        self.saldo -= jumlah
        return buat_id("EWL")
