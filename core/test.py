import asyncio

# # step-1
# get the current event loop/create a new one if necessary
loop = asyncio.get_event_loop()

# # run-1
# # run the event loop until it is stopped/manually interrupted
# loop.run_forever()
# # rest of the code will not be executed until the event loop is stopped

# # run-2
# # or, run the event loop until a certain condition is met
# # new
# loop.run_until_complete(asyncio.sleep(3))
# # rest of the code will be executed after 3 seconds

def task():
    import datetime
    print(f"Task executed at {datetime.datetime.now()}")

# # run-3
# # scheduling tasks as soon as possible if the event loop is running
# loop.call_soon(task)
# loop.call_soon(task)
# loop.call_soon(task)

# # opening the event loop 
# loop.run_until_complete(asyncio.sleep(5))

def trampoline(name:str = "")-> None:
    print(f"{name} is executing the trampoline function")

    # perform tasks here
    task()
    # schedule the trampoline function to be called again after a delay
    loop.call_later(.5, trampoline, name) # .5s delay

# # run once in the event loop
# loop.call_soon(trampoline, "first call")

# # run-4
# # start the event loop
# loop.run_until_complete(asyncio.sleep(5)) # run for 5 seconds before stopping the loop

# # run-5
# # instead of sleeping, we can stop it after a certain time
# loop.call_later(5, loop.stop) # stop the loop after 5 seconds

# loop.run_forever() # start the event loop and keep it running until stopped

# # run-6
# # we can schedule the trampoline function in the event loop more than once to see it in action
# loop.call_soon(trampoline, "first call")
# loop.call_soon(trampoline, "second call")
# loop.call_soon(trampoline, "third call")

# # start the event loop
# loop.run_until_complete(asyncio.sleep(8)) # run for 8 seconds before stopping the


def hog(name:str = "")-> None:
    print(f"{name} is hogging the CPU")
    sum = 0 
    for i in range(10000):
        for j in range(10000):
            sum += i * j 
    
# # run-7
loop.call_later(2,hog, "FIRST HOG") # schedule the hog function to run after 2 seconds
loop.call_soon(trampoline, "TRAMPOLINE CALL") # schedule the trampoline function to run as soon as possible
loop.set_debug(True) # enable debug mode to see the scheduling and execution of tasks in the event loop
# start the event loop
loop.run_until_complete(asyncio.sleep(6)) # run for 6 seconds before stopping the loop