from apscheduler.schedulers.blocking import BlockingScheduler

from app.commands.daily import main as daily
from app.commands.five_minutely import main as five_minutely

scheduler = BlockingScheduler()


scheduler.add_job(
    daily,
    trigger="interval",
    hours=24,
    id="cleanup_sessions",
)


scheduler.add_job(
    five_minutely,
    trigger="interval",
    minutes=5,
    id="hourly_job",
)


if __name__ == "__main__":
    scheduler.start()