import threading
import time

def sleeper(n, name):
    print("I am {}.  Going to sleep for {} seconds\n".format(name, n))
    time.sleep(n)
    print("{} has woken up from sleep\n".format(name))

t = threading.Thread(target=sleeper, name="thread1", args=(5, "thread1"))
t.start()
t.join() # <---- this is a blocking method

print("hi")