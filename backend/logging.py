from backend.models import Config, Log
from datetime import datetime

class Logging:
    def __init__(self, system_name):
        self.level = int(Config.objects.get(name="log_level_backend").value)
        self.system = system_name

    @property
    def date_time(self):
        format = "%Y-%m-%d %H:%M:%S"
        return datetime.now().strftime(format)
        
    #========================= LOGGER =====================#
    def logger(self, level, subsys, desc, save=False):
        if(save==True):
            Log(type=level, system=self.system, subsystem=subsys, user="System", description=desc).save()
        print(f"{self.date_time} {level.upper()} [{subsys}] => {desc}")

    #========================= DEBUG ======================#
    def debug(self, subsys, desc, save=False):
        if(self.level == 4):
            self.logger("debug", subsys, desc, save)

    #========================= INFO =======================#
    def info(self, subsys, desc, save=False):
        if((self.level == 3) or (self.level == 4)):
            self.logger("info", subsys, desc, save)

    #========================= WARNING ====================#
    def warning(self, subsys, desc, save=False):
        if((self.level == 2) or (self.level == 3) or (self.level == 4)):
            self.logger("warning", subsys, desc, save)
    
    #========================= ERROR ======================#
    def error(self, subsys, desc, save=False):
        if((self.level == 1) or (self.level == 2) or (self.level == 3) or (self.level == 4)):
            self.logger("error", subsys, desc, save)