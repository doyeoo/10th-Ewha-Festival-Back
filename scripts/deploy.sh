cd home/ubuntu/app

source venv/bin/activate

pip install -r requirement.txt
python manage.py collectstatic
python manage.py migrate
deactivate
sudo systemctl restart uwsgi
