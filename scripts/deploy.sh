cd /home/ubuntu/app

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python manage.py collectstatic
python manage.py migrate
deactivate
sudo systemctl restart uwsgi
