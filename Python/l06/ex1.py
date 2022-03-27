import bs4
import urllib.request
import re

processed_pages = []
result = []


def crawl(start_page, distance, action):
    global processed_pages
    global result

    if start_page in processed_pages or distance <= 0:
        return

    processed_pages.append(start_page)
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

                crawl(ref, distance - 1, action)
                result.append((ref, action(ref)))
    except:
        return


def contains(page, expression):
    automat = re.compile(r"([^.^\n^?^!]*?" + expression + r"[^.^\n^?^!]*\.)")
    with urllib.request.urlopen(page) as fh:
        content = bs4.BeautifulSoup(fh.read(), 'html.parser')
        return [sentence.group() for sentence in automat.finditer(content.get_text())]


crawl('https://ii.uni.wroc.pl/', 2, lambda x: contains(x, "Python"))
print(result)
