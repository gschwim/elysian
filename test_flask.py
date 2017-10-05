from flask import Flask, jsonify
import tsxlib, json

ip='172.16.254.254'

app = Flask(__name__)

@app.route('/mount/getstatus', methods=['GET'])
def mount_status(ip='172.16.254.254'):
    mount = tsxlib.mount(ip)
    return jsonify(mount.GetStatus()['Parked'])

if __name__ == '__main__':
    app.run(debug=True, port=5555)
