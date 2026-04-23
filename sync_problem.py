import time
import requests
def fetch(url):
    response = requests.get(url)
    return response.json()

# This takes 6 seconds. Why??
def main():
    for url in ["https://jsonplaceholder.typicode.com/todos/1",
                "https://jsonplaceholder.typicode.com/todos/2",
                "https://jsonplaceholder.typicode.com/todos/3",
                "https://jsonplaceholder.typicode.com/todos/4",
                "https://jsonplaceholder.typicode.com/todos/5",
                "https://jsonplaceholder.typicode.com/todos/6",
                "https://jsonplaceholder.typicode.com/todos/7",
                ]:
        print(fetch(url))
    
if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()
    print(f"Total time taken: ~{t1 - t0:.2f} seconds")