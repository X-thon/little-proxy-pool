import time
from api import app
from getter import Getter
from detector import Detector
from multiprocessing import Process
from settings import API_HOST, API_PORT, API_THREADED

TESTER_CYCLE_INDEX = 60
GETTER_CYCLE_INDEX = 60
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True


class Scheduler(object):

    def schedule_detector(self, cycle_index=TESTER_CYCLE_INDEX):
        """
        定时测试代理
        """
        detector = Detector()
        while True:
            print("测试器开始运行")
            detector.run()
            time.sleep(cycle_index)

    def schedule_getter(self, cycle_index=GETTER_CYCLE_INDEX):
        """
        定时获取代理
        """
        getter = Getter()
        while True:
            print("开始抓取代理")
            getter.run()
            time.sleep(cycle_index)

    def schedule_api(self):
        """
        开启API
        """
        app.run(API_HOST, API_PORT)

    def run(self):
        """
        运行调度器
        """
        print("代理池开始运行")
        try:
            if TESTER_ENABLED:
                detector_process = Process(target=self.schedule_detector)
                detector_process.start()

            if GETTER_ENABLED:
                getter_process = Process(target=self.schedule_getter)
                getter_process.start()

            if API_ENABLED:
                api_process = Process(target=self.schedule_api)
                api_process.start()
        except KeyboardInterrupt:
            detector_process.terminate()
            getter_process.terminate()
            api_process.terminate()
        finally:
            detector_process.join()
            getter_process.join()
            api_process.join()


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()