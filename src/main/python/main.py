from fbs_runtime.application_context.PyQt5 import ApplicationContext
from gui import MainWindow

import sys

class AppContext(ApplicationContext):

    def __init__(self, *args, **kwargs):
        super(AppContext, self).__init__(*args, **kwargs)
        print('Init MainWindow')
        self.window = MainWindow(self)

    def run(self):
        self.window.show()
        return self.app.exec_()

if __name__ == '__main__':
    print('Init AppContext')
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)