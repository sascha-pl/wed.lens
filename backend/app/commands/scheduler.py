from apscheduler.schedulers.blocking import BlockingScheduler

from app.commands.daily import main as daily


scheduler = BlockingScheduler()


scheduler.add_job(
    daily,
    trigger="interval",
    hours=24,
    id="cleanup_sessions",
)


# scheduler.add_job(
#     some_hourly_job,
#     trigger="interval",
#     hours=1,
#     id="hourly_job",
# )


if __name__ == "__main__":
    scheduler.start()