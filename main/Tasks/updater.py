from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .download_link import create_download_link, delete_download_link
from .send_active_email import send_email
def start():
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.start()
    scheduler.add_job(create_download_link, 'interval', minutes=10, max_instances=100000000000000)
    scheduler.add_job(delete_download_link, 'interval', days=1)
    scheduler.add_job(send_email, 'interval', minutes=5)