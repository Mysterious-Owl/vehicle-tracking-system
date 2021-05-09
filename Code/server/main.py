from flask import Flask, render_template, request
import time
import csv

app = Flask(__name__, template_folder='templates')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
fieldnames = ['time', 'lat', 'long', 'id']
lat = ''
long = ''


def save_csv(uid):
    global lat
    global long
    if len(lat.split('.')[0]) != 4 or len(long.split('.')[0]) != 5:
        return False

    if lat[-1] == 'S':
        lat = '-' + lat
    elif lat[-1] == 'N':
        lat = '+' + lat

    if long[-1] == 'W':
        long = '-' + long
    elif long[-1] == 'E':
        long = '+' + long

    lat = lat[:-1]
    long = long[:-1]
    with open('data/data.csv', 'a', newline='') as f:
        csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
        f.seek(0, 2)
        if f.tell() == 0:
            csv_writer.writeheader()
        csv_writer.writerow({"time": time.strftime('%d-%m %H:%M'), "lat": lat, 'long': long, 'id': uid})
    return True


def read_data(file):
    with open(f'data/{file}.csv', 'r') as f:
        if file == 'data':
            data = list(csv.reader(f))[1:]
        elif file == 'user':
            user_f = csv.DictReader(f)
            data = {}
            for i in user_f:
                data[i['id']] = {'name': i['name'], 'color': i['color']}
    return data


def update_data():
    users_full = read_data('user')
    data = read_data('data')
    fdata = {}
    for i in data:
        try:
            fdata.__getitem__(users_full[i[3]]['name'])
        except KeyError:
            fdata[users_full[i[3]]['name']] = {'data': [], 'color': users_full[i[3]]['color']}
        finally:
            fdata[users_full[i[3]]['name']]['data'].append([i[0],
                                                            float(i[1][:3] + '.' + str(float(i[1][3:]) / 60)[2:8]),
                                                            float(i[2][:4] + '.' + str(float(i[2][4:]) / 60)[2:8])])
    last = [float(data[-1][1][:3] + '.' + str(float(data[-1][1][3:]) / 60)[2:8]),
            float(data[-1][2][:4] + '.' + str(float(data[-1][2][4:]) / 60)[2:8])]
    with open('static/where.js', 'w') as f:
        f.write(f'data = {str(fdata)};\nlast = {str(last)}')
    return


@app.route('/')
def hello_world():
    update_data()
    data = read_data('data')
    lat_temp = float(data[-1][1][:3] + '.' + str(float(data[-1][1][3:]) / 60)[2:])
    long_temp = float(data[-1][2][:4] + '.' + str(float(data[-1][2][4:]) / 60)[2:])
    return render_template('index.html', lat=str(lat_temp)[:10] + '°', long=str(long_temp)[:10] + '°')


@app.route('/add')
def add_data():
    global lat
    global long
    lat = request.args.get('lat', default='', type=str)
    long = request.args.get('long', default='', type=str)
    password = request.args.get('key', default='', type=str)
    uid = request.args.get('id', default=-1, type=int)
    if password == '' or lat == '' or long == '' or uid == -1:
        return "Missing argument(s)"
    elif password != 'aawaaraa':
        return "Wrong Key"
    elif not save_csv(uid):
        return "ERROR: Invalid Arguments"
    return f"{uid}:{lat}:{long}"


if __name__ == '__main__':
    app.run(debug=True)
