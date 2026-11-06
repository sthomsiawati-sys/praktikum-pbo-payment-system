import importlib
import pkgutil
 
 
def muat_semua_plugin() -> None:
    """Impor semua modul di folder plugins/ agar dekoratornya aktif."""
    for info in pkgutil.iter_modules(__path__):
        importlib.import_module(f"{__name__}.{info.name}")
