#!/usr/bin/python
from django_cron import CronJobBase, Schedule
from .models.backengine import Devicelogs42021,Devicelogs

class AttendanceCollector(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'swasthya.attendance_cron_job'    # a unique code

    def do(self):
        dv = Devicelogs42021.objects.using('second').all()
        dd = Devicelogs()
        for d in dv:
            dd.deviceid = d.deviceid
            #dd.save()
        print (str(dv))
        #print("This is a cron job print")    # do your thing here