import csv
from sale import Sale


class SalesCollection:
    def __init__(self):
        self.sales = []  # Lista vacía para almacenar los objetos Sale.

    def importar_ventas_CSV(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for sale_data in reader:
                # Llamamos a la clase Sale, pasandole los datos del CSV, creando un nuevo objeto Sale y añadiendolo a la lista de ventas.
                sale = Sale(
                    sale_id=sale_data['sale_id'],
                    client_id=int(sale_data['client_id']),
                    product=sale_data['product'],
                    category=sale_data['category'],
                    amount=float(sale_data['amount']),
                    date=sale_data['date']
                )
                # Añadimos las ventas del JSON a la lista de ventas de la clase SalesCollection.
                self.sales.append(sale)

    def sales_by_client(self, cliente_id):
        lista = []
        for sale in self.sales:
            if sale.client_id == int(cliente_id):
                lista.append(sale)
        # Devuelve una lista con las ventas que pertenecen al cliente especificado.
        return lista

    def total_amount_by_client(self, client_id):
        compras = self.sales_by_client(client_id)
        total = 0.0
        for compra in compras:
            total += compra.amount
        # Devuelve el total de las ventas realizadas por el cliente especificado.
        return total

    def total_amount_by_category(self, category):
        total = 0.0
        for sale in self.sales:
            if sale.category.lower() == category.lower():
                total += sale.amount
        # Devuelve el total de las ventas realizadas en la categoría especificada.
        return total

    def average_sale_by_client(self, client_id):
        compras = self.sales_by_client(client_id)
        if not compras:
            # Si el cliente no tiene compras, devuelve 0 para evitar división por cero.
            return 0.0
        total = self.total_amount_by_client(client_id)
        return total / len(compras)
