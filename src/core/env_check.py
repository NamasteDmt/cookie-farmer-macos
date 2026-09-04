import importlib, sys
def check_environment() -> dict:
    modules = ["patchright","humanization_playwright","pyanty","capsolver_core","psutil","pystray","plyer","caveman"]
    if sys.platform == "darwin": modules.append("pynput")
    else: modules.append("keyboard")
    results = {}
    for mod in modules:
        try:
            importlib.import_module(mod)
            results[mod] = "OK"
        except ImportError as e:
            results[mod] = f"Ошибка: {e}"
    return results
