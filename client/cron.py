from crontab import CronTab
from log import logger
import os

class Cron(object):
    def __init__(self):
        self.USER = os.getlogin()
        self.HOME = os.getenv("HOME")
        self.cron = CronTab(tabfile='/etc/crontab', user=self.USER)
        # self.removeJob()

    def setJob(self):
        try:
            logger.info("Cron: Setting job...")
            job = self.cron.new(command=self.HOME+'/svs/svs', comment='SVSystem')
            job.every_reboot()
            job.enable()
            # self.cron.write()
            self.cron.write_to_user( user=self.USER )
        except BaseException as e:
            logger.error("Cron error: %s", e)

        self.check()

    def check(self):
        jobs = self.findJobs()
        if not list(jobs):
            logger.warning("Cron: Job not set. Bad")
            self.setJob()
        else:
            logger.info("Cron: Job set and should start on bootup. Good")

    def removeJob(self):
        jobs = self.findJobs()
        for job in jobs:
            self.cron.remove( job )
        # self.cron.write()
        self.cron.write_to_user( user=self.USER )


    def findJobs(self):
        return self.cron.find_comment('SVSystem')
