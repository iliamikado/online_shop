import requests


if __name__ == '__main__':
    result = requests.post('http://192.168.0.110:8000/api/reserve', data={'username': 'Kate', 'item': 'Item 3'})
    print(result.text)
