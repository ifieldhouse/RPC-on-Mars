from rpc import RPC


rpc = RPC()
username = None

while True:

    prompt = f'¿Qué deseas hacer, {username}?' if username is not None else '¿Qué deseas hacer?'

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

    if option == '1':
        logs = rpc.get_logs()
        for log in logs:
            print(log)

    elif option == '2':
        msg = input('Escribe el mensaje a general: ')
        rpc.write_to_log(msg)

    elif option == '3':
        msg = input('Escriba su nombre: ')
        username = msg
        user = username
        rpc.set_name(msg)

    elif option == '4':
        if username == None:
            print('Usted es anónimo; no tiene mensajes.')
        else:
            logs = rpc.get_my_logs(username)
            for log in logs:
                print(logs)

    elif option == '5':
        users = rpc.get_users()
        for user in users:
            print(user)

    elif option == '6':
        target = input('Nombre del destinatario: ')
        msg = input('Mensaje a enviar: ')
        rpc.write_to_client_log(target, msg)

    elif option == '7':
        print('Saliendo del programa...')
        break
