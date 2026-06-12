import pydoc


def buscar_documentacion(termino: str) -> str:
    """Busca la documentación oficial de Python para un módulo, función o clase y la devuelve como texto."""
    try:
        doc = pydoc.render_doc(termino, renderer=pydoc.plaintext)
        return doc[:2000] + ("..." if len(doc) > 2000 else "")
    except Exception as e:
        return f"No se encontró documentación para '{termino}': {e}"
