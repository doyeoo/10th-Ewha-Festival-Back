cd /home/ubuntu/app

python3 -m venv venv
source venv/bin/activate

pip install -r requirement.txt
python3 manage.py collectstatic
python3 manage.py migrate
deactivate
sudo systemctl restart uwsgi
