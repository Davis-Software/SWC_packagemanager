import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher:
    def __init__(self, path, callback):
        self.observer = Observer()
        self.DIRECTORY_TO_WATCH = path
        self.callback = callback

    def run(self):
        event_handler = Handler(self.callback)
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    def __init__(self, callback):
        self.callback = callback

    def on_any_event(self, event):
        if event.is_directory:
            return None

        elif event.event_type in ['created', 'modified']:
            self.callback(event)

        else:
            pass


def run_daemon(path, callback):
    w = Watcher(path, callback)
    threading.Thread(target=w.run, daemon=True).start()


if __name__ == '__main__':
    def call(e):
        print("ok", e)
    run_daemon("/home/david/Desktop", call)
    while True:
        time.sleep(1) # keep process running