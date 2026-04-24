import json

try:
    from .client import Client
except ImportError:
    from client import Client


class ClientCollection:
    def __init__(self, clients=None):
        self.clients = clients if clients is not None else []  # Lista vacía para almacenar los objetos Client.

    def importar_clientes_JSON(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for client_data in data:
                # Llamamos a la clase Client, pasandole los datos del JSON, creando un nuevo objeto Client y añadiendolo a la lista de clientes.
                client = Client(
                    client_id=client_data['client_id'],
                    name=client_data['name'],
                    country=client_data['country'],
                    signup_date=client_data['signup_date']
                )
                # Añadimos los clientes del JSON a la lista de clientes de la clase ClientCollection.
                self.clients.append(client)

    def get_client_by_id(self, client_id):
        for client in self.clients:
            if client.client_id == client_id:
                return client
        return None  # Si no se encuentra el cliente, devuelve None.

    def clients_by_country(self, country):
        lista = []
        for client in self.clients:
            if client.country.lower() == country.lower():
                lista.append(client)
        return lista
