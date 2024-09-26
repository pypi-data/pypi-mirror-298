import tqdm
import traceback

class Executor:
    def __init__(self, max_workers:int, progressor:tqdm.tqdm| None = None) -> None:
        self.__progressor = progressor
        
    def __enter__(self):
        return self
        
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