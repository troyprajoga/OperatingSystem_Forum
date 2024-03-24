import threading
import random

LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000
buffer = []
lock = threading.Lock()
producer_finished = False
customers_finished = 0

def producer():
    global producer_finished
    for _ in range(MAX_COUNT):
        num = random.randint(LOWER_NUM, UPPER_NUM)
        with lock:
            buffer.append(num)
            with open("all.txt", "a") as file:
                file.write(str(num) + "\n")
    producer_finished = True

def customer_even():
    global customers_finished
    while not producer_finished or buffer:
        with lock:
            if buffer:
                num = buffer.pop()
                if num % 2 == 0:
                    with open("even.txt", "a") as file:
                        file.write(str(num) + "\n")
                    customers_finished += 1

def customer_odd():
    global customers_finished
    while not producer_finished or buffer:
        with lock:
            if buffer:
                num = buffer.pop()
                if num % 2 != 0:
                    with open("odd.txt", "a") as file:
                        file.write(str(num) + "\n")
                    customers_finished += 1

if __name__ == "__main__":
    producer_thread = threading.Thread(target=producer)
    customer_even_thread = threading.Thread(target=customer_even)
    customer_odd_thread = threading.Thread(target=customer_odd)

    producer_thread.start()
    customer_even_thread.start()
    customer_odd_thread.start()

    producer_thread.join()
    customer_even_thread.join()
    customer_odd_thread.join()

    print("Execution Complete")
