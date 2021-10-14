from flask import Flask, request
import json

app = Flask(__name__)


@app.route("/api/reserve", methods=['POST'])
def reserve():
    name = request.form.get('username')
    item = request.form.get('item')

    if not name:
        return 'authorization error'
    if not item:
        return 'item was not provided'

    statistic = dict()
    with open('data.json', 'r', encoding='utf-8') as file:
        statistic = json.load(file)

    if item not in statistic['data'] or statistic['data'][item] == 0:
        return 'Do not have this item'

    for user in statistic['users']:
        if user['name'] == name:
            user[item] = user.get(item, 0) + 1
            break
    else:
        statistic['users'].append({'name': name, item: 1})

    statistic['data'][item] -= 1

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(statistic, file)
    return 'new stats here'


@app.route("/api/stats", methods=['GET'])
def stats():
    statistic = dict()
    with open('data.json', 'r', encoding='utf-8') as file:
        statistic = json.load(file)
    return statistic


if __name__ == '__main__':
    with open('../data/parameters.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    app.run(host=config['server_address'], port=config['server_port'], debug=True)
