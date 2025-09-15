from itertools import zip_longest

# Datos “paralelos” (mismo orden que PRODUCTOS)
PRECIOS = [" 19.90 ", "9,50", "129.00", " 4.99", "7.00"]
STOCK   = [10, 0, 5, 25, 3]  # unidades

# pipeline.py

# Dataset inicial de ejemplo (simula datos desordenados de un CSV)
PRODUCTOS = [
    "   Teclado USB   ",
    "RATÓN inalámbrico",
    " monitor 24'' ",
    "CABLE HDMI ",
    " alfombrilla  "
]


CATEGORIAS = ["perifericos", "perifericos", "monitores", "cables", "otros"]


def normalizar_lista(datos):
    # TODO: limpiar espacios y pasar a minúsculas
    pass

if __name__ == "__main__":
    print("Original:", PRODUCTOS)
    print("Normalizado:", normalizar_lista(PRODUCTOS))



def to_float(s: str) -> float:
    return float(s.strip().replace(",", "."))

def normalizar_precio_lista(precios):
    # TODO: map -> float limpio
    pass

def combinar_catalogo(nombres_norm, precios_float, stock):
    """
    Devuelve una lista de tuplas/dicts uniendo nombre-precio-stock,
    filtrando los artículos sin stock (>0).
    """
    # TODO: zip + filter (stock > 0)
    pass

def aplicar_descuento(items, porcentaje: float):
    """Devuelve items con un precio_final tras aplicar % descuento."""
    # TODO: map con dict actualizado
    pass

if __name__ == "__main__":
    # ---- Fase 1
    print("Original:", PRODUCTOS)
    normalizado = normalizar_lista(PRODUCTOS)
    print("Normalizado:", normalizado)
    capitalizados = list(map(lambda s: s.title(), normalizado))
    print("Capitalizados:", capitalizados)
    resumen = [(p.upper(), len(p)) for p in capitalizados]
    print("Resumen:", resumen)

    # ---- Fase 2
    precios = normalizar_precio_lista(PRECIOS)
    print("Precios:", precios)

    catalogo = combinar_catalogo(normalizado, precios, STOCK)
    print("Catálogo con stock:", catalogo)

    catalogo_desc = aplicar_descuento(catalogo, 10.0)  # 10% dto.
    print("Catálogo con descuento:", catalogo_desc)



from functools import reduce

def kpis_catalogo(items):
    """
    items: lista de dicts con al menos: nombre, precio, stock, (opcional) precio_final
    Devuelve un dict con KPIs agregados.
    """
    # total de referencias (tras filtros)
    total_refs = len(items)

    # suma de unidades en stock
    total_unidades = reduce(lambda acc, it: acc + it["stock"], items, 0)

    # valor bruto (precio * stock)
    valor_inventario = reduce(lambda acc, it: acc + it["precio"] * it["stock"], items, 0.0)

    # si hay precio_final, calcula valor con descuento; si no, usa precio
    valor_final = reduce(
        lambda acc, it: acc + (it.get("precio_final", it["precio"])) * it["stock"],
        items,
        0.0
    )

    # media de precio unitario (evita división por cero)
    media_precio = (
        reduce(lambda acc, it: acc + it["precio"], items, 0.0) / total_refs
        if total_refs else 0.0
    )

    return {
        "total_refs": total_refs,
        "total_unidades": total_unidades,
        "valor_inventario": round(valor_inventario, 2),
        "valor_final": round(valor_final, 2),
        "media_precio": round(media_precio, 2),
    }

def calidad_datos(nombres_norm, precios_float, stock):
    """
    Valida condiciones globales con any/all sobre colecciones paralelas.
    """
    # ¿Algún precio <= 0?
    hay_precios_no_validos = any(p <= 0 for p in precios_float)

    # ¿Todos los nombres no vacíos tras normalización?
    nombres_ok = all(n.strip() for n in nombres_norm)

    # ¿Hay algún stock negativo?
    hay_stock_negativo = any(s < 0 for s in stock)

    # ¿Listas sincronizadas?
    longitudes_ok = len(nombres_norm) == len(precios_float) == len(stock)

    return {
        "hay_precios_no_validos": hay_precios_no_validos,
        "nombres_ok": nombres_ok,
        "hay_stock_negativo": hay_stock_negativo,
        "longitudes_ok": longitudes_ok,
    }

if __name__ == "__main__":
    # ---- Fase 1
    print("Original:", PRODUCTOS)
    normalizado = normalizar_lista(PRODUCTOS)
    print("Normalizado:", normalizado)
    capitalizados = list(map(lambda s: s.title(), normalizado))
    print("Capitalizados:", capitalizados)
    resumen = [(p.upper(), len(p)) for p in capitalizados]
    print("Resumen:", resumen)

    # ---- Fase 2
    precios = normalizar_precio_lista(PRECIOS)
    print("Precios:", precios)

    catalogo = combinar_catalogo(normalizado, precios, STOCK)
    print("Catálogo con stock:", catalogo)

    catalogo_desc = aplicar_descuento(catalogo, 10.0)  # 10% dto.
    print("Catálogo con descuento:", catalogo_desc)

    # ---- Fase 3
    kpis = kpis_catalogo(catalogo_desc)
    print("KPIs:", kpis)

    calidad = calidad_datos(normalizado, precios, STOCK)
    print("Calidad de datos:", calidad)   





    #kpis por familia





    def combinar_catalogo_con_categoria(nombres_norm, precios_float, stock, categorias):
        combinado = zip_longest(nombres_norm, precios_float, stock, categorias, fillvalue=None)
        completos = filter(lambda t: all(v is not None for v in t), combinado)
        con_stock = filter(lambda t: t[2]>0, completos)
        return [{"nombre": n, "precio": p, "stock":s, "categoria":c}   for (n,p,s,c) in con_stock] 
    

    def kpi_por_categoria(items_con_cat):
        
        def acum(acc,it):
                cat = it["categoria"]
                val = it['precio'] * it['stock']
                acc[cat] = acc.get(cat, 0.0) + val  # suma si ya existe, inicializa a 0.0 si no
                return acc

        resultado = reduce(acum, items_con_cat, {})




    catalogo_cat = combinar_catalogo_con_categoria(normalizado, precios, STOCK, CATEGORIAS )

    print("KPI por categoria:", kpi_por_categoria(catalogo_cat))