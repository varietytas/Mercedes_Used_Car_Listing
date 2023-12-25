from flask import Flask, request, send_file
from os import path
import rp


app = Flask(__name__)


@app.route('/<filesname>', methods=["GET"])
def data_request(filesname):
    type_arg = request.args.get('type')

    if type_arg == '0':
        return send_file(path.join('.', 'static', f'{filesname}.png'), mimetype='image/png') 
    elif type_arg == '1':
        return send_file(path.join('.', 'static', f'{filesname}.txt'))


@app.route('/mean', methods=["POST"])
def mean_request():
    value = rp.request_procession(
        int(request.form['lowest']),
        int(request.form['highest'])
    )
    return str(value)


if __name__ == "__main__":
    app.run()
