'''
Proyecto final del curso "Programador Python [ID: PP-18-20230511]"
Opción "Blog"

Autor: Julian Griffin

'''

import requests



if __name__ == "__main__":
    
    usuario = str(input("Ingrese el nombre del usuario que desea borrar:\n"))

    delete_url = f'http://127.0.0.1:5000/posteos/{usuario}'

    response = requests.delete(delete_url)

    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Error: {response.status_code}")