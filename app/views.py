from app import app, jar_path, db
from app.models import Server
from flask import render_template, jsonify
from flask.ext.security import login_required

import os
import errno
import subprocess
import psutil


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/start')
def start_server():
    server = Server.query.first()
    if server:
        p = run_jar()
        server.pid = p.pid
    else:
        server = Server()
        p = run_jar()
        server.pid = p.pid
    db.session.commit()
    status = pid_exists(p.pid)
    return jsonify({'running': status})

@app.route('/stop')
def stop_server():
    server = Server.query.first()
    p = psutil.Process(server.pid)
    p.terminate()
    server.pid = None
    db.session.commit()
    return {'running': False}

@app.route('/status')
def checkstatus():
    server = Server.query.first()
    return pid_exists(server.pid)

# http://stackoverflow.com/questions/568271/how-to-check-if-there-exists-a-process-with-a-given-pid
def pid_exists(pid):
    """Check whether pid exists in the current process table.
    UNIX only.
    """
    if pid < 0:
        return False
    if pid == 0:
        # According to "man 2 kill" PID 0 refers to every process
        # in the process group of the calling process.
        # On certain systems 0 is a valid PID but we have no way
        # to know that in a portable fashion.
        raise ValueError('invalid PID 0')
    try:
        os.kill(pid, 0)
    except OSError as err:
        if err.errno == errno.ESRCH:
            # ESRCH == No such process
            return False
        elif err.errno == errno.EPERM:
            # EPERM clearly means there's a process to deny access to
            return True
        else:
            # According to "man 2 kill" possible error values are
            # (EINVAL, EPERM, ESRCH)
            raise
    else:
        return True


def run_jar():
    return subprocess.Popen(['java', '-jar', jar_path], stdout=subprocess.PIPE)
