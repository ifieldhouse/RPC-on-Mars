#!/usr/bin/env python3

import rpc


lib = rpc.RPC()
username = None

prompt = f'¿Qué deseas hacer, {username}?' if username is not None else '¿Qué deseas hacer?'

print(prompt)
print(lib)
option = input('Escriba su opción: ')

if option == '1':
    ans = lib.add(2, b=3)
    print(ans)

elif option == '0':
    print('Saliendo del programa...')
