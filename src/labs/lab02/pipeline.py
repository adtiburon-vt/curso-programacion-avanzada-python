from itertools import zip_longest
from functools import reduce

# Dataset inicial de ejemplo (simula datos desordenados de un CSV)
PRODUCTOS = [
    "   Teclado USB   ",
    "RATÓN inalámbrico",
    " monitor 24'' ",
    "CABLE HDMI ",
    " alfombrilla  ",
    " alfombrilla  "
]


def normalizar_lista(datos):
    return [item.strip().lower() for item in datos]

def buscar_producto(letra):
    return [elem for elem in list(map(
        lambda s: s.title(), normalizar_lista(PRODUCTOS)
    )) if elem[0] == letra.upper()]

# Datos “paralelos” (mismo orden que PRODUCTOS)
PRECIOS = [" 19.90 ", "9,50", "129.00", " 4.99", "7.00"]
STOCK   = [10, 0, 5, 25, 3]  # unidades

def to_float(s: str) -> float:
    return float(s.strip().replace(",", "."))

def normalizar_precio_lista(precios):
    return list(map(to_float, precios))

def combinar_catalogo(nombres_norm, precios_float, stock):
    """
    Devuelve una lista de tuplas/dicts uniendo nombre-precio-stock,
    filtrando los artículos sin stock (>0).
    """
    combinado = list(zip_longest(nombres_norm, precios_float, stock))
    con_stock = filter(lambda t: t[2] or 0 > 0, combinado)
    # Devuelve dicts legibles
    return [{"nombre": n, "precio": p, "stock": s} for (n, p, s) in con_stock]

def aplicar_descuento(items, porcentaje: float):
    """Devuelve items con un precio_final tras aplicar % descuento."""
    factor = (100.0 - porcentaje) / 100.0
    return list(map(
        lambda it: {**it, "precio_final": round(it.get("precio_final", it['precio']) * factor, 2)},
        items
    ))

def descuentos_encadenados(items, *porcentajes):
    for descuento in porcentajes:
        items = aplicar_descuento(items, descuento)
    return items

def top_n(*items, n=2):
    return sorted(*items, key=lambda x: x['precio']*x['stock'], reverse=True)[:n]

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
    print('Fase 1:\n------\n')
    print("Original:", PRODUCTOS)
    normalizado = normalizar_lista(PRODUCTOS)
    # print("Normalizado:", normalizado)

    capitalizados = list(map(lambda s: s.title(), normalizado))
    print("Capitalizados:", capitalizados)

    '''
    resumen = [(p.upper(), len(p)) for p in capitalizados]
    print("Resumen:", resumen)
    
    diccionario = {nombre: long for nombre, long in resumen}
    print('Diccionario:', diccionario)

    cjto = {nombre for nombre in capitalizados}
    print('Conjunto:', cjto)

    p = buscar_producto('a')
    print('Productos que empiezan por "A":', p)
    '''
    # ---- Fase 2
    print('\n\nFase 2:\n------\n')
    precios = normalizar_precio_lista(PRECIOS)
    print("Precios:", precios)

    catalogo = combinar_catalogo(capitalizados, precios, STOCK)
    print("\nCatálogo con stock:", catalogo)

    catalogo_desc = aplicar_descuento(catalogo, 10.0)  # 10% dto.
    print("\nCatálogo con descuento:", catalogo_desc)
    
    """catalogo_desc_multiple = descuentos_encadenados(catalogo, 10.0, 10.0)  # 10% dto.
    print("\nCatálogo con descuento múltiple:", catalogo_desc_multiple)

    top_2 = top_n(catalogo)
    print('Top 2:', top_2)"""

    # ---- Fase 3
    print('\n\nFase 3:\n------\n')
    kpis = kpis_catalogo(catalogo_desc)
    print("KPIs:", kpis)

    calidad = calidad_datos(capitalizados, precios, STOCK)
    print("\nCalidad de datos:", calidad)
