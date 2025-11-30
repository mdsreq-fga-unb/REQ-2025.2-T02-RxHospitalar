import inspect

#teste da instância dos filtros de estoque
def test_estoque_filters_instancia(dummy_parent):
    from app.views.components.estoque_filters import EstoqueFilterFrame
    f = EstoqueFilterFrame(parent=dummy_parent)
    assert f

#teste de variáveis e callbacks dos filtros de estoque
def test_estoque_filters_vars_e_callbacks(dummy_parent):
    from app.views.components.estoque_filters import EstoqueFilterFrame
    f = EstoqueFilterFrame(parent=dummy_parent)

    for attr in dir(f):
        if attr.endswith("_var"):
            var = getattr(f, attr)
            if hasattr(var, "set"):
                var.set("TESTE")

    callable_names = [n for n in dir(f) if any(n.startswith(p) for p in ("on_", "_on", "apply", "filtrar"))]
    for name in callable_names:
        m = getattr(f, name)
        if callable(m):
            sig = inspect.signature(m)
            if all(p.default is not inspect._empty or p.kind in (p.VAR_POSITIONAL, p.VAR_KEYWORD)
                   for p in sig.parameters.values()):
                m()

#teste de busca dos filtros do estoque
def test_estoque_filters_busca(dummy_parent):
    from app.views.components.estoque_filters import EstoqueFilterFrame
    f = EstoqueFilterFrame(parent=dummy_parent)
    for attr in dir(f):
        if "search" in attr and attr.endswith("_var"):
            var = getattr(f, attr)
            if hasattr(var, "set"):
                var.set("ABC")
                assert var.get() == "ABC"