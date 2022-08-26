cd /home/ubuntu/app

python -m venv venv
source venv/bin/activate

sudo apt-get install python-pip
pip install -r requirements.txt
python manage.py collectstatic
python manage.py migrate
deactivate
sudo systemctl restart uwsgi
