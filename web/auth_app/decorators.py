from threading import Thread


def execute_in_background(function):
    def start_thread(*args, **kwargs):
        thread = Thread(target=function, args=args, kwargs=kwargs)
        thread.start()

    return start_thread
