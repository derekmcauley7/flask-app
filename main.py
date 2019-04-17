from flask import Flask, json, request
import os

app = Flask(__name__)


@app.route("/status")
def index():
    cpus, host_name, ip, mem_gib = get_variables()
    data = ({"hostname": host_name,
             "ip_address": ip,
             "cpus": cpus,
             "memory": mem_gib,
             })

    response = create_json_response(data)
    return response


def create_json_response(data):
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


def get_variables():
    mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    mem_gib = mem_bytes / (1024. ** 3)
    host_name = request.base_url
    ip = request.host.split(':')[0]
    cpus = os.cpu_count()
    return cpus, host_name, ip, mem_gib


if __name__ == "__main__":
    app.run(port=8080)
