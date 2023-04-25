import concurrent.futures ,logging ,time,random,queue,math
class crochet :
    def __init__(self,function,data:list,workers:int,loading_call):
        self.process_func = function
        self.num_workers = workers
        self.loading_call = loading_call
        self.done_data = queue.Queue()
        self.completed , self.total = 0 , len(data)
        self.data = data
        self.load_fraction = 1000
        self.name = "crochet_worker"
    def run(self) :
        # format data 
        self.f_data = enumerate(self.data) # add an index to each data bit so that it can be rearanged later
        # start 
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers,thread_name_prefix=self.name) as workers :
            workers.map(self.worker_wrapper,self.f_data)
        # sort list
        self.processed_data = [None]*self.done_data.qsize()
        for item in range(self.done_data.qsize()) :
            index,data = self.done_data.get_nowait()
            self.processed_data[index] = data
        return self.processed_data
    def worker_wrapper(self,unproccesed_data):
        index,data = unproccesed_data
        new_data = self.process_func(data)
        self.done_data.put((index,new_data))
        self.completed += 1
        self.load_call()
        return
    def load_call(self):
        if self.completed%(self.total//self.load_fraction)==0:
            self.loading_call(self.completed/self.total)