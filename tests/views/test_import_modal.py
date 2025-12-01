import inspect

#teste da importação das instâncias do modal
def test_loading_import_modal_instancia(dummy_parent):
    from app.views.components.loading_import_modal import LoadingImportModal
    m = LoadingImportModal(dummy_parent)
    assert m

#teste da importação dos métodos do modal
def test_loading_import_modal_metodos(dummy_parent):
    from app.views.components.loading_import_modal import LoadingImportModal
    m = LoadingImportModal(dummy_parent)
    for name in dir(m):
        if any(k in name.lower() for k in ("start", "close", "update", "finish", "destroy", "status")):
            fn = getattr(m, name)
            if callable(fn):
                sig = inspect.signature(fn)
                if all(p.default is not inspect._empty or p.kind in (p.VAR_POSITIONAL, p.VAR_KEYWORD)
                       for p in sig.parameters.values()):
                    # Chama métodos sem argumentos obrigatórios
                    try:
                        fn()
                    except Exception:
                        pass