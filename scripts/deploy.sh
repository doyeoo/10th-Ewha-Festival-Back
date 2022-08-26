cd /home/ubuntu/app

apt-get install python3-venv
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python3 manage.py collectstatic
python3 manage.py migrate
deactivate
sudo systemctl restart uwsgi
