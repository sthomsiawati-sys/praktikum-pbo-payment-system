from core.notifiers import ConsoleNotifier
from core.processor import PaymentProcessor
from core.registry import buat_metode
from plugins import muat_semua_plugin

muat_semua_plugin()
p = PaymentProcessor(ConsoleNotifier())

va = buat_metode("va", tagihan=500_000)
print("status awal :", va.status)
p.checkout(va, 500_000, "mhs@utr.ac.id")
print("status akhir:", va.status)
p.checkout(va, 500_000, "mhs@utr.ac.id")   # bayar lagi -> ditolak