import csv
import hashlib
import datetime
from tko.settings.settings import Settings
import enum
import os

class LogAction(enum.Enum):
    NONE = 'NONE'
    OPEN = 'OPEN'
    DOWN = 'DOWN'
    FREE = 'FREE' 
    TEST = 'TEST' # CORRECT|WRONG|COMPILE|RUNTIME
    SELF = 'SELF' # int
    QUIT = 'QUIT'


class ActionData:
    def __init__(self, timestamp: str, action_id: str, rep: str = "", task: str = "", payload: str = ""):
        self.timestamp = timestamp
        self.action: str = action_id
        self.rep = rep
        self.task = task
        self.payload = payload
        self.hash = ""

    def action_self_same_task(self, other):
        return self.action == LogAction.SELF and other.action == LogAction.SELF and self.rep == other.rep and self.task == other.task

    def __str__(self):
        return f'{self.timestamp}, {self.action}, {self.rep}, {self.task}, {self.payload}'

class Logger:
    instance = None
    COMP_ERROR = "COMPILATION_ERROR"
    grade_action_cache: str | None = None

    @staticmethod
    def get_instance():
        if Logger.instance is None:
            Logger.instance = Logger()
        return Logger.instance

    def __init__(self):
        self.settings: Settings | None = None
        self.last_hash: str = ""
        self.rep_alias: str = ""
        self.cached_action: ActionData | None = None

    def get_settings(self) -> Settings:
        if self.settings is None:
            raise Exception("Settings not set")
        return self.settings

    def set_settings(self, settings: Settings):
        self.settings = settings
        return self

    def set_rep(self, rep_alias: str):
        self.rep_alias = rep_alias
        self.last_hash = self.get_last_hash()
        return self

    def get_last_hash(self) -> str:
        # open csv file and get last hash
        log_file = self.get_log_file()
        if not os.path.exists(log_file):
            return ""
        with open(log_file, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            if len(rows) == 0:
                return ""
            return rows[-1][0]

    def check_log_file_integrity(self):
        log_file = self.get_log_file()
        if not os.path.exists(log_file):
            return False
        with open(log_file, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            for i in range(1, len(rows)):
                hash_anterior = rows[i-1][0]

                hash = rows[i][0]
                timestamp = rows[i][1]
                action = rows[i][2]
                rep = rows[i][3]
                task = rows[i][4]
                payload = rows[i][5]

                action_data = ActionData(timestamp, action, rep, task, payload)
                calc_hash = self.generate_hash(action_data, hash_anterior)
                if calc_hash != hash:
                    print('Erro de continuidade na linha {}: {}'.format(str(i + 1).rjust(4), rows[i]))
        return True


    def get_log_file(self):
        rootdir = self.get_settings().app.get_rootdir()
        log_file = "rep_log.csv"
        return os.path.join(rootdir, self.rep_alias, log_file)

    @staticmethod
    def generate_hash(action_data: ActionData, last_hash: str):
        comprimento = 6
        input_str = str(action_data) + last_hash
        hash_completo = hashlib.sha256(input_str.encode()).hexdigest()
        return hash_completo[:comprimento]  # Retorna os primeiros 'comprimento' caracteres do hash

    def push_to_file(self, action_data: ActionData):
        action_data.hash = self.generate_hash(action_data, self.last_hash)
        
        with open(self.get_log_file(), 'a', newline='') as file:
            writer = csv.writer(file)
            ad = action_data
            writer.writerow([ad.hash, ad.timestamp, ad.action, ad.rep, ad.task, ad.payload])
            self.last_hash = ad.hash

    def store_in_cached(self, action_data: ActionData) -> bool:
        if self.cached_action is None and action_data.action == LogAction.SELF:
            return True
        if self.cached_action is not None and self.cached_action.action_self_same_task(action_data):
            return True
        return False

    def record_event(self, action: LogAction, task: str = "", payload: str = ""):
        if self.rep_alias == "":
            return
        action_data = ActionData(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), action.value, self.rep_alias, task, payload)
        
        if self.store_in_cached(action_data):
            self.cached_action = action_data
            return
        
        if self.cached_action is not None:
            self.push_to_file(self.cached_action)
            self.cached_action = None
        
        if self.store_in_cached(action_data):
            self.cached_action = action_data
        else:
            self.push_to_file(action_data)