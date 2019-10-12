import rpc

# Ejemplo de uso librería rpc
rpc = rpc.rpc()

username = None

while True:
    if username == None:
        prompt = "¿Qué desea hacer?"
    else:
        prompt = f"¿Qué desea hacer, {username}?"
    option = input(f"""
{prompt}
(1) Ver mensajes en 'General'
(2) Enviar mensaje a 'General'
(3) Definir su nombre
(4) Ver tus mensajes
(5) Ver usuarios disponibles
(6) Enviar mensaje a usuario
(7) Salir
Escriba su opción: """)
    if option == "1":
        print(rpc.get_logs())
    elif option == "2":
        msg = input("Escribe el mensaje a general: ")
        rpc.write_to_log(msg)
    elif option == "3":
        msg = input("Escriba su nombre: ")
        username = msg
        user = username
        rpc.set_name(msg)
    elif option == "4":
        if username == None:
            print("Usted es anónimo, no tiene mensajes.")
            continue
        your_logs = rpc.get_my_logs(username)
        print(your_logs)
    elif option == "5":
        users = rpc.get_users()
        print(users)
    elif option == "6":
        target = input("Nombre de usuario a quien le quiere enviar el mensaje: ")
        msg = input("Mensaje que le quiere enviar: ")
        rpc.write_to_client_log(target, msg)
    elif option == "7":
        print("Saliendo del programa...")
        break

