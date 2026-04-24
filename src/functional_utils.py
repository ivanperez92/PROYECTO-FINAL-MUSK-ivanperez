def filtrar_ventas_por_categoria(lista_de_objetos_ventas, categoria_a_buscar):
    """
    Usa FILTER y LAMBDA para devolver solo las ventas de una categoría.
    Se usará para el Cálculo 8.
    """
    # filter() recibe dos cosas: una condición (lambda) y una lista.
    # La lambda dice: "Para cada 'venta', mira si su categoría coincide con la buscada".
    ventas_filtradas = filter(
        lambda venta: venta.category.lower() == categoria_a_buscar.lower(),
        lista_de_objetos_ventas
    )

    # Convertimos el resultado de filter a una lista normal de Python
    return list(ventas_filtradas)


def extraer_mes_y_monto(lista_de_objetos_ventas):
    """
    Usa MAP y LAMBDA para transformar objetos Sale en diccionarios de Mes/Monto.
    Se usará para el Cálculo 10.
    """
    # map() transforma cada elemento de la lista original.
    # La lambda toma el objeto venta y devuelve un diccionario simplificado.
    datos_simplificados = map(
        lambda venta: {
            # Extrae los primeros 7 caracteres para agrupar por mes: "YYYY-MM"
            "mes": venta.date[:7],
            "monto": venta.amount
        },
        lista_de_objetos_ventas
    )

    return list(datos_simplificados)
