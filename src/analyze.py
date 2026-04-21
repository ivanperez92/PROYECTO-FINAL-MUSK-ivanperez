from collections import defaultdict
import os
import json
import pandas as pd
from client_collection import ClientCollection
from sales_collection import SalesCollection
from functional_utils import filtrar_ventas_por_categoria, extraer_mes_y_monto


def analyze():
    # 1. CARGA DE DATOS
    mis_clientes = ClientCollection()
    mis_ventas = SalesCollection()

    # Obtener la ruta del directorio padre (raíz del proyecto), ya que aveces no lo lo encuentra correctamente.
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    clients_path = os.path.join(project_root, 'data', 'clients.json')
    sales_path = os.path.join(project_root, 'data', 'sales.csv')

    mis_clientes.importar_clientes_JSON(clients_path)
    mis_ventas.importar_ventas_CSV(sales_path)

    # 1. Número total de clientes:
    total_clientes = len(mis_clientes.clients)
    print(f"Número total de clientes: {total_clientes}")

    # 2. Número total de ventas:
    total_ventas = len(mis_ventas.sales)
    print(f"Número total de ventas: {total_ventas}")

    # 3. Total de ingresos por cliente:

    resumen_clientes = []

    print("\n=== RESUMEN POR CLIENTE ===")
    for cliente in mis_clientes.clients:
        total_gastado = mis_ventas.total_amount_by_client(cliente.client_id)
        # 4. Número de ventas por cliente:
        numero_ventas = len(mis_ventas.sales_by_client(cliente.client_id))
        # 5. Promedio de ventas por cliente:
        promedio_ventas = mis_ventas.average_sale_by_client(cliente.client_id)

        resumen_clientes.append({
            "client_id": cliente.client_id,
            "name": cliente.name,
            "total_spent": total_gastado,
            "sale_count": numero_ventas,
            "average_sale": promedio_ventas
        })

        # Print para verificar los datos
        print(f"Cliente: {cliente.name} (ID: {cliente.client_id})")
        print(f"  Total gastado: {total_gastado}")
        print(f"  Número de ventas: {numero_ventas}")
        print(f"  Promedio por venta: {promedio_ventas}\n")

    # 6. Cliente con mayor gasto por país: Versión mejorada y más limpia

    def cliente_mayor_gasto_por_pais(clientes_collection, ventas_collection):
        # 1. Agrupar clientes por país
        clientes_por_pais = defaultdict(list)
        for cliente in clientes_collection.clients:
            clientes_por_pais[cliente.country].append(cliente)

        resultados_paises = {}

        # 2. Para cada país, encontrar el cliente con mayor gasto
        for pais, lista_clientes in clientes_por_pais.items():
            if not lista_clientes:
                continue

            # Usar max() para encontrar al mejor cliente
            cliente_max_gasto = max(
                lista_clientes,
                key=lambda cliente: ventas_collection.total_amount_by_client(
                    cliente.client_id)
            )

            # Guardamos el nombre en el diccionario
            resultados_paises[pais] = cliente_max_gasto.name

            print(f"País: {pais} | Cliente: {cliente_max_gasto.name}")

        return resultados_paises

    print("\n=== CLIENTE CON MAYOR GASTO POR PAÍS ===")
    # Llamamos a la función y guardamos el resultado
    top_por_pais = cliente_mayor_gasto_por_pais(mis_clientes, mis_ventas)

    # 7. Total de ventas por categoría: usando pandas para simplificar el proceso.
    print("\n=== TOTAL DE VENTAS POR CATEGORÍA ===")

    def calcular_ventas_por_categoria(coleccion_de_ventas):
        # Sale se convierta a sí mismo en diccionario.
        lista_diccionarios = [venta.to_dict()
                              for venta in coleccion_de_ventas.sales]

        # Creamos la tabla
        tabla_ventas = pd.DataFrame(lista_diccionarios)

        # Agrupamos y sumamos
        resultado = tabla_ventas.groupby('category')['amount'].sum()

        return resultado.to_dict()

    ventas_por_categoria_final = calcular_ventas_por_categoria(mis_ventas)

    # Imprimimos el resultado para verificar
    for categoria, total in ventas_por_categoria_final.items():
        print(f"Categoría: {categoria} | Total: {total:.2f}€")

# 8. Cliente con más ventas en una categoría específica
    print("\n=== CLIENTE CON MÁS VENTAS EN UNA CATEGORÍA ===")

    def cliente_con_mas_compras_en_categoria(coleccion_clientes, coleccion_ventas, categoria_objetivo):
        # PASO FUNCIONAL: Usamos la utilidad para obtener solo las ventas de esa categoría
        ventas_filtradas = filtrar_ventas_por_categoria(
            coleccion_ventas.sales, categoria_objetivo)

        if not ventas_filtradas:
            return "No hay ventas en esta categoría", 0

        # PASO DE LÓGICA: Contamos cuántas veces aparece cada ID de cliente
        conteo_de_ids = {}  # Diccionario: {id_cliente: cantidad_de_compras}

        for venta in ventas_filtradas:
            id_cliente = venta.client_id
            # Si el ID ya está en el diccionario sumamos 1, si no, empezamos en 1
            conteo_de_ids[id_cliente] = conteo_de_ids.get(id_cliente, 0) + 1

        # PASO DE BÚSQUEDA: Encontramos el ID que tiene el valor más alto
        id_max = max(conteo_de_ids, key=conteo_de_ids.get)
        cantidad_compras = conteo_de_ids[id_max]

        # Obtenemos el nombre del cliente usando su ID
        objeto_cliente = coleccion_clientes.get_client_by_id(id_max)
        nombre_cliente = objeto_cliente.name if objeto_cliente else "Desconocido"

        return nombre_cliente, cantidad_compras

    categoria = "Electronics"
    nombre_top, total_compras = cliente_con_mas_compras_en_categoria(
        mis_clientes, mis_ventas, categoria)

    print(f"En la categoría '{categoria}':")
    print(
        f"El cliente con más compras es {nombre_top}. (Realizó {total_compras} compras).")

    # 9. Número de clientes que superan un gasto mínimo (ej. 500€)
    print("\n=== CLIENTES QUE SUPERAN EL GASTO MÍNIMO ===")

    def calcular_clientes_superan_gasto_minimo(clientes_collection, ventas_collection, gasto_minimo):
        clientes_superan = []
        for cliente in clientes_collection.clients:
            total_gastado = ventas_collection.total_amount_by_client(
                cliente.client_id)
            if total_gastado > gasto_minimo:
                clientes_superan.append((cliente.name, total_gastado))
        return clientes_superan

    gasto_minimo = 500.0
    clientes_superan_gasto = calcular_clientes_superan_gasto_minimo(
        mis_clientes, mis_ventas, gasto_minimo)
    for nombre, total in clientes_superan_gasto:
        print(f"Cliente: {nombre} | Total gastado: {total:.2f}€")


# 10. Ventas acumuladas mes a mes
    print("\n=== EVOLUCIÓN MENSUAL DE VENTAS ===")

    def calcular_evolucion_mensual(ventas_collection):
        # (Functional_utils): Extraemos solo los datos que nos interesan (mes y monto)
        datos_mes_monto = extraer_mes_y_monto(ventas_collection.sales)

        # (Pandas): Convertimos esa lista de diccionarios en una tabla
        tabla_mensual = pd.DataFrame(datos_mes_monto)

        # (Agrupación): Agrupamos por la columna 'mes' y sumamos la columna 'monto'
        ventas_por_mes_series = tabla_mensual.groupby('mes')['monto'].sum()

        # Convertimos el resultado de Pandas (que es una Serie) a un diccionario normal
        return ventas_por_mes_series.to_dict()

    evolucion_ventas = calcular_evolucion_mensual(mis_ventas)

    for mes, total in evolucion_ventas.items():
        print(f"Mes: {mes} | Total recaudado: {total:.2f}€")


# GENERACIÓN DEL INFORME JSON FINAL

    # 1. Calculamos el ingreso total acumulado de todos los clientes(usando los datos ya procesados)
    total_revenue_global = sum(c['total_spent'] for c in resumen_clientes)

    # 2. Limpiamos la lista de clientes para que solo muestre el nombre.
    nombres_high_spending = [nombre for nombre,
                             monto in clientes_superan_gasto]

    # 3. Creamos el diccionario con la estructura del PDF
    reporte_final = {
        "summary": {
            "total_clients": total_clientes,
            "total_sales": total_ventas,
            "total_revenue": round(total_revenue_global, 2)
        },
        "clients": resumen_clientes,
        "top_client_by_country": top_por_pais,
        "sales_by_category": ventas_por_categoria_final,
        "high_spending_clients": nombres_high_spending,
        "monthly_sales": evolucion_ventas
    }

    # 4. Gestión de carpetas: Creamos 'reports' si no existe
    reports_dir = os.path.join(project_root, 'reports')
    os.makedirs(reports_dir, exist_ok=True)

    report_path = os.path.join(reports_dir, 'reporte_final.json')

    # 5. Guardado del archivo
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(reporte_final, f, indent=4, ensure_ascii=False)

    print(f"\n✅ PROCESO FINALIZADO. Reporte creado en: {report_path}")


if __name__ == "__main__":
    analyze()
