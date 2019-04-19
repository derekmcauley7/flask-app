import subprocess
from subprocess import PIPE
from flask import Flask, json
import os

app = Flask(__name__)

@app.route("/status")
def index():
    cpus, host_name, ip, mem_gib = get_json_variables()
    data = ({"hostname": host_name,
             "ip_address": ip,
             "cpus": cpus,
             "memory": mem_gib,
             })

    response = create_response(data)
    return response

def create_response(data):
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


def get_json_variables():
    host_name = get_host_name()
    ip = get_ip()
    mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    mem_gib = mem_bytes / (1024. ** 3)
    cpus = get_cpu()
    return cpus, host_name, ip, mem_gib


def get_ip():
    ip = subprocess.run(["hostname", "-I"], stdout=PIPE, stderr=PIPE)
    stdout = ip.stdout.decode()
    stdout.rstrip()
    ip = stdout.rstrip()
    return ip


def get_host_name():
    host_name = subprocess.run(["hostname"], stdout=PIPE, stderr=PIPE)
    stdout = host_name.stdout.decode()
    stdout.rstrip()
    host_name = stdout.rstrip()
    return host_name


def get_cpu():
    cpu = subprocess.run(["egrep", "-c", "^processor", "/proc/cpuinfo"], stdout=PIPE, stderr=PIPE)
    stdout = cpu.stdout.decode()
    stdout.rstrip()
    cpu = stdout.rstrip()
    return cpu


if __name__ == '__main__':
    # Debug/Development
    app.run(debug=True, host="0.0.0.0", port="8080")
