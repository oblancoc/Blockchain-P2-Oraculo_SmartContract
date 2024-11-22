from web3 import Web3
import requests
import random

#Conexión a Sepolia usando Infura

infura_url = str(input("Ingresa tu URL ejemplo, https://sepolia.infura.io/v3/YOUR_PROJECT_ID:"))
web3 = Web3(Web3.HTTPProvider(infura_url))

# Verificar conexión
if web3.is_connected():
    print("Conectado a la red Sepolia")
else:
    print("Error al conectar a la red Sepolia")


# Convertir la dirección a formato checksum

addres_contract = str(input("Ingresa la dirección del contrato:"))
contract_address = web3.to_checksum_address(addres_contract)


contract_abi = [
   ##Colocar el ABI aquí...
]

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Configuración de la cuenta y clave privada

account_wallet = str(input("ingresa tu dirección de cuenta de tu Wallet, por ejemplo MetaMask:"))
account = web3.to_checksum_address(account_wallet)  # Dirección de tu cuenta MetaMask convertida checksum
print(f"Cuenta en formato checksum: {account}")


private_key = str(input("Ingresa tu Private key: "))     # Clave privada asociada (OJO ESTA CLAVE NO DEBERÍA SER COMPARTIDA)

# Validar que la clave privada corresponde a la dirección. 

derived_address = Web3().eth.account.from_key(private_key).address
print(f"Dirección derivada de la clave privada: {derived_address}")

if derived_address != account:
    raise ValueError("La clave privada no corresponde a la dirección configurada.")



#Función para obtener datos externos simulados (o desde una API real)

def fetch_external_data():
   
         # Ejemplo: Simular datos desde una fuente externa o API
        data = {
             

            "espacios_disponibles": random.randint(5,50),  # Número actualizado de espacios disponibles
            "precio_por_hora": random.randint(10,500)       # Precio por hora del espacio en Wei
        }
        print(f"Datos obtenidos: {data}")
        return data
   

# Función para actualizar los datos en el contrato

def update_contract():
    # Obtener datos externos
    data = fetch_external_data()
    
    # Asignar variables
    espacios_disponibles = data["espacios_disponibles"]
    precio_por_hora = data["precio_por_hora"]
    

    # Validar dirección y obtener nonce
    if not web3.is_checksum_address(account):
        raise ValueError("La dirección no está en formato checksum.")
	
    nonce = web3.eth.get_transaction_count(account)
    print(f"Nonce obtenido: {nonce}")
    

    # Construir la transacción para actualizar datos
    

    transaction = contract.functions.actualizarDatos(
        espacios_disponibles, precio_por_hora
    ).build_transaction({
        'chainId': 11155111,
        'gas': 200000,
        'gasPrice': web3.to_wei('20', 'gwei'),
        'nonce': nonce
    })
    

    # Firmar y enviar la transacción
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    print(f'Transacción enviada. Hash: {web3.to_hex(tx_hash)}')
    
balance = web3.eth.get_balance(account)
print(f"Saldo actual: {web3.from_wei(balance, 'ether')} ETH")


    

# 6. Ejecutar la actualización
update_contract()
