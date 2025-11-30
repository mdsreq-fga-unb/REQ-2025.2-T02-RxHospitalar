#arquivo para configuração dos testes pro Frontend incluindo os widgets e atributos que vêm com eles
import sys, types, pytest

try:
    import tkinter  # noqa
    from PIL import Image, ImageTk, ImageDraw  # noqa
except Exception:
    tk_mod = types.ModuleType("tkinter")
    ttk_mod = types.ModuleType("tkinter.ttk")

    widget_names = [
    "Frame", "Label", "Button", "Entry", "Combobox",
    "Radiobutton", "Checkbutton", "Separator", "Toplevel", "Style",
    "Menubutton", "Menu", "PhotoImage", "Canvas",
    "Progressbar", "Notebook", "Treeview", "Scrollbar"  
    ]

    class _DummyWidget:
        def __init__(self, *a, **k): self._v = ""; self._items = {}
        def pack(self, *a, **k): pass
        def pack_forget(self, *a, **k): pass
        def start(self, *a, **k): pass
        def stop(self, *a, **k): pass
        def grid(self, *a, **k): pass
        def place(self, *a, **k): pass
        def config(self, *a, **k): pass
        def configure(self, *a, **k): pass
        def cget(self, *a, **k): return ""
        def destroy(self): pass
        def bind(self, *a, **k): return 1
        def columnconfigure(self, *a, **k): pass
        def rowconfigure(self, *a, **k): pass
        def set(self, v): self._v = v
        def get(self): return getattr(self, "_v", "")
        def current(self, idx): pass
        def insert(self, idx, val): pass
        def delete(self, first, last=None): pass
        def pack_propagate(self, *a, **k): pass
        # indexação estilo dict (ex.: widget["menu"] = menu)
        def __setitem__(self, key, value): self._items[key] = value
        def __getitem__(self, key): return self._items.get(key)
        def __contains__(self, key): return key in self._items
        # ttk-specific helpers
        def state(self, *a, **k): return []
        def instate(self, *a, **k): return True
        def invoke(self, *a, **k): pass
        # Menu API
        def add_command(self, *a, **k): pass
        def add_cascade(self, *a, **k): pass
        def entryconfig(self, *a, **k): pass
        def index(self, *a, **k): return 0
        def post(self, *a, **k): pass
        def unpost(self, *a, **k): pass
        # Métodos de janela/modal
        def title(self, *a, **k): pass
        def geometry(self, *a, **k): pass
        def overrideredirect(self, *a, **k): pass
        def transient(self, *a, **k): pass
        def lift(self, *a, **k): pass
        def deiconify(self, *a, **k): pass
        def protocol(self, *a, **k): pass
        def focus_set(self, *a, **k): pass
        def grab_set(self, *a, **k): pass
        def grab_release(self, *a, **k): pass
        def withdraw(self, *a, **k): pass
        def attributes(self, *a, **k): pass
        def update_idletasks(self, *a, **k): pass
        def winfo_rootx(self): return 0
        def winfo_rooty(self): return 0
        def winfo_width(self): return 100
        def winfo_height(self): return 100
        def winfo_reqwidth(self): return 100
        def winfo_reqheight(self): return 100
        def winfo_screenwidth(self): return 1920
        def winfo_screenheight(self): return 1080
        # Métodos extras comuns
        def event_generate(self, *a, **k): pass
        def after(self, *a, **k): pass
        def after_cancel(self, *a, **k): pass
        def winfo_children(self): return []
        def winfo_toplevel(self): return self
        def winfo_exists(self): return True
        def winfo_ismapped(self): return True
        def winfo_manager(self): return ""
        def winfo_class(self): return "Frame"
        def winfo_id(self): return 1
        def winfo_name(self): return "dummy"
        def winfo_parent(self): return ""
        def winfo_viewable(self): return True
        def winfo_geometry(self): return "100x100+0+0"
        def winfo_screenmmwidth(self): return 300
        def winfo_screenmmheight(self): return 200
        def winfo_fpixels(self, *a, **k): return 1.0
        def winfo_pixels(self, *a, **k): return 1
        def winfo_pointerx(self): return 0
        def winfo_pointery(self): return 0
        def winfo_pointerxy(self): return (0, 0)
        def winfo_screen(self): return ""
        def winfo_visual(self): return ""
        def winfo_visualid(self): return 0
        def winfo_visualsavailable(self): return []
        def winfo_colormapfull(self): return False
        def winfo_colormapwindows(self): return []
        def winfo_depth(self): return 24
        def winfo_screenvisual(self): return ""
        def winfo_server(self): return ""
        def winfo_vrootheight(self): return 100
        def winfo_vrootwidth(self): return 100
        def winfo_vrootx(self): return 0
        def winfo_vrooty(self): return 0

    #cria classes dummy
    for w in widget_names:
        setattr(ttk_mod, w, type(w, (_DummyWidget,), {}))
        setattr(tk_mod, w, type(w, (_DummyWidget,), {}))

    # ttk.Style específico com métodos esperados
    class _DummyStyle(_DummyWidget):
        def map(self, *a, **k): pass
        def configure(self, *a, **k): pass
        def theme_use(self, *a, **k): return "default"
        def layout(self, *a, **k): return {}
        def lookup(self, *a, **k): return None
    ttk_mod.Style = _DummyStyle  # override para garantir métodos

    class _BaseVar:
        def __init__(self, *a, **k): self._v = ""
        def get(self): return self._v
        def set(self, v): self._v = v

    class _BoolVar(_BaseVar):
        def set(self, v): self._v = bool(v)
        def get(self): return bool(self._v)

    tk_mod.StringVar = _BaseVar
    tk_mod.BooleanVar = _BoolVar
    tk_mod.IntVar = _BaseVar
    tk_mod.ttk = ttk_mod

    # PIL stubs
    pil_pkg = types.ModuleType("PIL")
    img_mod = types.ModuleType("PIL.Image")
    imgtk_mod = types.ModuleType("PIL.ImageTk")
    imgdraw_mod = types.ModuleType("PIL.ImageDraw")

    class _Img:
        def resize(self, *a, **k): return self
    img_mod.open = lambda *a, **k: _Img()
    imgtk_mod.PhotoImage = lambda *a, **k: None
    imgdraw_mod.Draw = lambda *a, **k: None

    sys.modules["tkinter"] = tk_mod
    sys.modules["tkinter.ttk"] = ttk_mod
    sys.modules["PIL"] = pil_pkg
    sys.modules["PIL.Image"] = img_mod
    sys.modules["PIL.ImageTk"] = imgtk_mod
    sys.modules["PIL.ImageDraw"] = imgdraw_mod

@pytest.fixture
def dummy_parent():
    class DummyParent(_DummyWidget):
        pass
    return DummyParent()