from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import tqdm
import traceback


class ThreadPool:
    def __init__(self, max_workers:int, progressor:tqdm.tqdm| None = None) -> None:
        self.__progressor = progressor
        self.__executor = ThreadPoolExecutor(max_workers=max_workers)
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
        for _ in range(20):
            self.__executor.shutdown()
        return True
        
    def __progress_update(self, fut):
        if fut.exception():
            print("Exception in Thread.")
            print(fut.result())
        elif fut.cancelled():
            print("Thread is Cancelled.")
            print(fut.result())
        elif fut.done():
            if isinstance(self.__progressor, tqdm.tqdm):
                self.__progressor.update(1)
            elif self.__progressor is None:
                pass
        else: 
            print("Thread is terminated at half way.")
            print(fut.result())

            
    def submit(self, func, *args):
        fut = self.__executor.submit(func, *args)
        fut.add_done_callback(self.__progress_update)