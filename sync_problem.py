import time

def fetch(url):
    # blocking i/o operation wasting time
    time.sleep(2)  # simulating network a call
    return f"Got {url}"

# This takes 6 seconds. Why??
def main():
    for url in ["url1", "url2", "url3"]:
        print(fetch(url))
    
if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()
    print(f"Total time taken: ~{t1 - t0:.2f} seconds")