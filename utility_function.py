import logging
import logging.handlers
class EasyLogger:

    def __init__(self, logfile = 'logging.txt'):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        self.fileHandler = logging.FileHandler(logfile, encoding='utf-8')
        self.streamHander = logging.StreamHandler()
        self.fileHandler.setFormatter(self.formatter)
        self.streamHander.setFormatter(self.formatter)
        self.logger.addHandler(self.fileHandler)
        self.logger.addHandler(self.streamHander)
        self.logger_level_list = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]

    def util_log(self, logger_level = 1):
        self.logger.setLevel(self.logger_level_list[logger_level])
        def wrapper(func):
            def decorator(*args, **kwargs):
                self.logger.info('{}  {}'.format(func.__name__,args,kwargs))
                res = func(*args, **kwargs)
                self.logger.info('{}'.format(res))
                return res
            return decorator
        return wrapper

    def log_info(self, log, logger_level = 1):
        self.logger.setLevel(self.logger_level_list[logger_level])
        self.logger.info('{}'.format(log))

if __name__ == '__main__':
    '''
    사용예시
    '''
    a = EasyLogger()

    @a.util_log(1)
    def printa(a,b):
        print(a,b)


    printa(1,2)
