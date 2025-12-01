import inspect

#teste da instância do navbar
def test_navbar_instancia(dummy_parent):
    from app.views.components.navbar import Header
    nb = Header(parent=dummy_parent)
    assert nb

#teste da alternância dos temas escuro e claro
def test_navbar_toggle_tematico(dummy_parent):
    from app.views.components.navbar import Header
    nb = Header(parent=dummy_parent)
    toggles = [n for n in dir(nb) if "toggle" in n.lower() or "theme" in n.lower()]
    for name in toggles:
        m = getattr(nb, name)
        if callable(m):
            sig = inspect.signature(m)
            if all(p.default is not inspect._empty or p.kind in (p.VAR_POSITIONAL, p.VAR_KEYWORD)
                   for p in sig.parameters.values()):
                m()

#teste para callbacks genéricos da navbar
def test_navbar_callbacks_genericos(dummy_parent):
    from app.views.components.navbar import Header
    nb = Header(parent=dummy_parent)
    candidates = [n for n in dir(nb) if any(n.startswith(p) for p in ("on_", "_on", "go", "nav"))]
    for name in candidates:
        m = getattr(nb, name)
        if callable(m):
            sig = inspect.signature(m)
            if all(p.default is not inspect._empty or p.kind in (p.VAR_POSITIONAL, p.VAR_KEYWORD)
                   for p in sig.parameters.values()):
                m()