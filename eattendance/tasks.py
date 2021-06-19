from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from models.backengine import DeviceLogs_4_2021, Ins

logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="mark_attendance",
    ignore_result=True
)
def mark_attendance():
    ins = Ins()
    ins.ins = "testing...."
    ins.save()
    print('task running...')
    logger.info("Saved Attendance")