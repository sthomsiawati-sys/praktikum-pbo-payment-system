from core.notifiers import TelegramNotifier
from core.protocols import Notifier
from core.processor import PaymentProcessor
from core.registry import buat_metode
from plugins import muat_semua_plugin
 
muat_semua_plugin()
tg = TelegramNotifier()
print("isinstance(TelegramNotifier(), Notifier):", isinstance(tg, Notifier))
p = PaymentProcessor(tg)
p.checkout(buat_metode("qris"), 50_000, "@mahasiswa")
