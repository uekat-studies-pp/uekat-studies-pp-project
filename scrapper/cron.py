from crontab import CronTab
import os

script_file = os.getcwd() + "/main.py"

cron = CronTab(user='root')
job = cron.new(command='python ' + script_file)
job.second.every(1)
cron.write()
