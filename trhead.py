import threading , queue , time

class crochet : # opporation function
    # opporation function
    # data
    # numb of worker threads
    # loading bar function
    # 
    #
    #
    #
    #

    def __init__(self,function,data:list,threads:int,load):
        self.queue_to_do = queue.Queue()
        self.queue_done = queue.Queue()
        self.data_length = len(data)
        self.completed = 0
        self.worker_threads = []
        self.threads = threads
        self.output = [None] * self.data_length
        self.proccess_func = function
        self.load_func = load
        self.data_to_proccess = data

        # make worker threads 
        for thread in range(threads) :
            thread_name = f"worker {thread}"
            self.worker_threads.append(threading.Thread(
                target=self.thread_wraper,
                args=(self,),
                daemon=True,
                name=thread_name
                ))
            
        # start worker threads

        for worker in self.worker_threads :
            worker.start()

        # start adding data to out queue

        for index , data in self.data_to_proccess :
            self.queue_to_do.put((index,data))
            if self.queue_done.empty() == False :
                proccessed_data = self.queue_done.get()
                self.output[proccessed_data[0]] == proccessed_data[1]
                self.completed += 1
                self.status_update()
        
        while self.completed < self.data_length :
            proccessed_data = self.queue_done.get()
            self.output[proccessed_data[0]==proccessed_data[1]]
            self.completed += 1
            self.status_update()
        
        return self.output
            
    def status_update(self):
        self.load_func(self)
    
    def thread_wraper(self):
        while self.queue_to_do.unfinished_tasks == 0 : # wait till there are tasks to be done
            pass
        while True :
            data = self.queue_to_do.get() # get thing to do from queue , data comes in format (index,data)

            if data == "stop" : return # if data == stop flag , exit thread

            proccessed_data = self.proccess_func(data[1])
            self.queue_done.put((data[0],proccessed_data))
        

        
data = range(20)

def loadbar(info:crochet):
    percent = 100*(info.completed/info.data_length)
    print(f"{percent:.2f}%")

out = crochet(opporation,data,1,loadbar)