import bs4
import urllib.request
import re
import threading

processed_pages = []
result = []

lock_processed = threading.Lock()
lock_result = threading.Lock()


def crawl(start_page, distance, action):
    global processed_pages
    global result
    global lock_processed
    global lock_result

    if start_page in processed_pages or distance <= 0:
        return
    lock_processed.acquire()
    processed_pages.append(start_page)
    lock_processed.release()

    threads = list()

    # Ignore open error messages (pages that require login)
    try:
        with urllib.request.urlopen(start_page) as fh:
            content = bs4.BeautifulSoup(fh.read(), 'html.parser')

            for ref in [link.get('href') for link in content.find_all('a')]:
                if ref == None:
                    continue

                # Relative link
                if "http" not in ref:
                    start_page = start_page[:-
                                            1] if start_page[-1] == "/" else start_page
                    ref = ref[1:] if ref[0] == "/" else ref
                    ref = start_page + "/" + ref

                x = threading.Thread(
                    target=crawl, args=(ref, distance - 1, action))
                threads.append(x)
                x.start()

                lock_result.acquire()
                result.append((ref, action(ref)))
                lock_result.release()
    except:
        return

    for t in threads:
        t.join()


def contains(page, expression):
    automat = re.compile(r"([^.^\n^?^!]*?" + expression + r"[^.^\n^?^!]*\.)")
    with urllib.request.urlopen(page) as fh:
        content = bs4.BeautifulSoup(fh.read(), 'html.parser')
        return [sentence.group() for sentence in automat.finditer(content.get_text())]


crawl('https://ii.uni.wroc.pl/', 2, lambda x: contains(x, "Python"))
print(result)
