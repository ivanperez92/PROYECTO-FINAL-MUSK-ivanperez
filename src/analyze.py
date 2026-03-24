from .client_collection import ClientCollection
from .sales_collection import SalesCollection
import json
import pandas as pd
import os
from collections import defaultdict


def analyze():
    # 1. CARGA DE DATOS
    mis_clientes = ClientCollection()
    mis_ventas = SalesCollection()

    # Obtener la ruta del directorio padre (raíz del proyecto)
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
            "total_gastado": total_gastado,
            "numero_ventas": numero_ventas,
            "promedio_ventas": promedio_ventas
        })

        # Print para verificar los datos
        print(f"Cliente: {cliente.name} (ID: {cliente.client_id})")
        print(f"  Total gastado: {total_gastado}")
        print(f"  Número de ventas: {numero_ventas}")
        print(f"  Promedio por venta: {promedio_ventas}\n")

    # 6. Cliente con mayor gasto por país: Versión mejorada y más limpia
    def cliente_mayor_gasto_por_pais(clientes_collection, ventas_collection):
    
        # Agrupar clientes por país usando defaultdict (más eficiente)
        clientes_por_pais = defaultdict(list)
        for cliente in clientes_collection.clients:
            clientes_por_pais[cliente.country].append(cliente)
        
        # Para cada país, encontrar el cliente con mayor gasto
        for pais, lista_clientes in clientes_por_pais.items():
            if not lista_clientes:  # Saltar si no hay clientes en este país
                continue
                
            # Usar max() con key function para encontrar el cliente con mayor gasto
            cliente_top = max(
                lista_clientes,
                key=lambda cliente: ventas_collection.total_amount_by_client(cliente.client_id)
            )
            
            # Calcular el gasto total del cliente top
            gasto_total = ventas_collection.total_amount_by_client(cliente_top.client_id)
            
            print(f"País: {pais}")
            print(f"  Cliente: {cliente_top.name} (ID: {cliente_top.client_id})")
            print(f"  Gasto total: {gasto_total}")
            print()

    print("\n=== CLIENTE CON MAYOR GASTO POR PAÍS ===")
    cliente_mayor_gasto_por_pais(mis_clientes, mis_ventas)
