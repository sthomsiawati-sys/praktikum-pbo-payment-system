from typing import Protocol, runtime_checkable
 
 
@runtime_checkable
class Notifier(Protocol):
    """Objek apa pun dengan method kirim() dianggap Notifier."""
 
    def kirim(self, penerima: str, pesan: str) -> None: ...
