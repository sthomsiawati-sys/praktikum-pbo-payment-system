from core.base import PaymentMethod, PembayaranGagal
from core.protocols import Notifier
from core.utils import rupiah
 
 
class PaymentProcessor:
    """Memproses checkout tanpa peduli metode bayar dan kanal notifikasi."""
 
    def __init__(self, notifier: Notifier):
        if not isinstance(notifier, Notifier):
            raise TypeError(
                "notifier harus memiliki method kirim(penerima, pesan)"
            )
        self.notifier = notifier
        self.riwayat: list[tuple[str, str, float]] = []
 
    def checkout(
        self, metode: PaymentMethod, jumlah: float, pelanggan: str
    ) -> bool:
        try:
            trx_id = metode.proses(jumlah)
        except PembayaranGagal as err:
            self.notifier.kirim(pelanggan, f"Pembayaran gagal: {err}")
            return False
 
        self.riwayat.append((trx_id, metode.nama, jumlah))
        self.notifier.kirim(
            pelanggan,
            f"Pembayaran {rupiah(jumlah)} via {metode.nama} berhasil. "
            f"ID: {trx_id}",
        )
        return True
