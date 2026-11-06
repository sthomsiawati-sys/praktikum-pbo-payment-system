class ConsoleNotifier:
    def kirim(self, penerima: str, pesan: str) -> None:
        print(f"[CONSOLE] ke {penerima}: {pesan}")
 
 
class EmailNotifier:
    def __init__(self, server: str = "smtp.kampus.ac.id"):
        self.server = server
 
    def kirim(self, penerima: str, pesan: str) -> None:
        print(f"[EMAIL via {self.server}] ke {penerima}: {pesan}")
 
 
class WhatsAppNotifier:
    def kirim(self, penerima: str, pesan: str) -> None:
        print(f"[WHATSAPP] ke {penerima}: {pesan}")
