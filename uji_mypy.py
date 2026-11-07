from core.processor import PaymentProcessor
from core.protocols import Notifier


class NotifierSalah:
    def kirim(self) -> None:  # parameter penerima dan pesan hilang
        print("terkirim")


n = NotifierSalah()
print("isinstance:", isinstance(n, Notifier))
pemroses = PaymentProcessor(n)  # <- mypy menandai baris ini
print("PaymentProcessor berhasil dibuat tanpa galat")