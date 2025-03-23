import requests
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import sys
import os

stop_event = threading.Event()
threads_to_run = 10
def check_url(url):
    try:
        response = requests.get(url, timeout=3)
        return url, response.status_code
    except requests.RequestException as e:
        return url, None  # Return None for any request errors

def log_found_url(url):
    """Append found URLs to a file."""
    absolute_path = os.path.join(os.path.dirname(__file__), "found.txt")
    with open(absolute_path, 'a') as f:
        #f.write(f"{url}\n")  --> base URL
        f.write(f"{url}\n")

def non_recursive_bust(base_url, wordlist):
    """Attempt to find directories and files without recursion using multithreading."""
    with ThreadPoolExecutor(max_workers=threads_to_run) as executor: 
        future_to_url = {executor.submit(check_url, urljoin(base_url, entry)): entry for entry in wordlist}

        for future in as_completed(future_to_url):
            if stop_event.is_set():  
                print("Stopping non-recursive busting...")
                break

            entry = future_to_url[future]
            try:
                url, status_code = future.result()
                if status_code is not None:
                    print(f"{url} - Status Code: {status_code}")
                    if status_code == 200:
                        print(f"[+] Found: {url}")
                        log_found_url(url)
            except Exception as e:
                print(f"Error processing {entry}: {e}")

def recursive_bust(base_url, wordlist, depth=0, max_depth=2):
    """Recursively attempt to find directories and files using multithreading."""
    if depth > max_depth:
        return


    with ThreadPoolExecutor(max_workers=threads_to_run) as executor:
        future_to_url = {executor.submit(check_url, urljoin(base_url, entry)): entry for entry in wordlist}

        for future in as_completed(future_to_url):
            if stop_event.is_set():
                print("Stopping recursive busting...")
                break

            entry = future_to_url[future]
            try:
                url, status_code = future.result()
                if status_code is not None:
                    print(f"{url} - Status Code: {status_code}")
                    if status_code == 200:
                        print(f"[+] Found: {url}")
                        log_found_url(url)
                        if url.endswith('/'):
                            recursive_bust(url, wordlist, depth + 1, max_depth)
            except Exception as e:
                print(f"Error processing {entry}: {e}")
        

def load_wordlist(file_path):
    """Load the wordlist from a file."""
    absolute_path = os.path.join(os.path.dirname(__file__), file_path)
    with open(absolute_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def main():
    try:
        target_url = input("Enter the target URL (e.g., http://example.com/): ")
        wordlist_path = input("Enter the path to the wordlist file: ")
        
        # Load the wordlist
        wordlist = load_wordlist(wordlist_path)

        # Ask the user which method to use
        method = input("Choose a method (1 for Non-Recursive, 2 for Recursive): ")
        threads_to_run = input("Enter Number of threads to run simultaneously (default=10 press: ENTER): ")
        
        if threads_to_run == "":
            threads_to_run = 10
        else:
            threads_to_run = int(threads_to_run)
       	    if(threads_to_run>20):
       	    	threads_to_run=20
        print("Threads set (MAX-20):",threads_to_run)    
        
        if method == '1':
            print("Starting non-recursive directory busting...")
            non_recursive_bust(target_url, wordlist)
        elif method == '2':
            print("Starting recursive directory busting...")
            recursive_bust(target_url, wordlist)
        else:
            print("Invalid choice. Please select 1 or 2.")
    except KeyboardInterrupt:
        print("\nCtrl+C pressed. Exiting...")
        stop_event.set() 
        sys.exit(0) 

if __name__ == "__main__":
    main()
