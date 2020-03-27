# start.sh

source /home/ahmad/Desktop/SmartCard/env/bin/activate

export FLASK_APP=wsgi.py
export FLASK_DEBUG=1
flask run

