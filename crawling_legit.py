import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import os

# pengambilan index
MAX_DOMAINS = 70000
START_DOMAIN_INDEX = 61000
MAX_URLS_PER_DOMAIN = 2
OUTPUT_CSV = "legitimate_urls2.csv"

ALLOWED_TLDS = (
    ".com",
    ".co.id",
    ".edu",
    ".org",
    ".net"
)

SHORTENER_DOMAINS = (
    "bit.ly", "t.co", "goo.gl", "tinyurl.com",
    "ow.ly", "buff.ly", "l.wl.co"
)

MIN_URL_LENGTH = 15
MAX_URL_LENGTH = 150
MIN_PATH_SEGMENTS = 1

REQUEST_TIMEOUT = 5
CRAWL_DELAY = 0.5

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (compatible; LegitCrawler/1.0)"
})

def is_allowed_domain(domain):
    return domain.lower().endswith(ALLOWED_TLDS)

def is_shortener(url):
    try:
        netloc = urlparse(url).netloc.lower()
        return any(s in netloc for s in SHORTENER_DOMAINS)
    except:
        return True

def is_good_legit_internal_url(url):
    try:
        parsed = urlparse(url)

        if is_shortener(url):
            return False

        if not (MIN_URL_LENGTH <= len(url) <= MAX_URL_LENGTH):
            return False

        path_segments = [p for p in parsed.path.split("/") if p]
        if len(path_segments) < MIN_PATH_SEGMENTS:
            return False

        return True
    except:
        return False

def fetch_page(url):
    try:
        r = session.get(url, timeout=REQUEST_TIMEOUT)

        if r.status_code == 403:
            print("[BLOCKED] 403 Forbidden:", url)
            return None, "blocked"

        if r.status_code == 429:
            print("[RATE LIMIT] 429 Too Many Requests:", url)
            return None, "rate_limit"

        if r.status_code != 200:
            return None, "error"

        if "text/html" not in r.headers.get("Content-Type", ""):
            return None, "non_html"

        return r.text, "ok"

    except requests.exceptions.Timeout:
        print("[TIMEOUT]", url)
        return None, "timeout"
    except requests.exceptions.RequestException:
        print("[REQUEST ERROR]", url)
        return None, "error"

def get_internal_links(url, domain_netloc):
    html, status = fetch_page(url)
    if status != "ok":
        return [], status

    soup = BeautifulSoup(html, "html.parser")
    links = set()

    for a in soup.find_all("a", href=True, limit=80):
        full_url = urljoin(url, a["href"])
        parsed = urlparse(full_url)

        if parsed.netloc == domain_netloc and is_good_legit_internal_url(full_url):
            links.add(full_url)

    return list(links), "ok"

def crawl_domain(start_url, max_urls):
    domain_netloc = urlparse(start_url).netloc
    visited = set([start_url])
    collected = []

    links, status = get_internal_links(start_url, domain_netloc)

    if status in ["blocked", "rate_limit"]:
        return collected, status

    for link in links:
        if link not in visited:
            visited.add(link)
            collected.append(link)

            if len(collected) >= max_urls:
                break

        time.sleep(CRAWL_DELAY)

    return collected, "ok"

if __name__ == "__main__":
    df = pd.read_csv("domains_only.csv")
    df = df[df["Domain"].apply(is_allowed_domain)]

    domains = df["Domain"].head(MAX_DOMAINS).tolist()
    total_domains = len(domains)

    print("Total domain valid:", total_domains)
    print("Mulai crawling dari domain ke:", START_DOMAIN_INDEX)

    if os.path.exists(OUTPUT_CSV):
        os.remove(OUTPUT_CSV)

    global_start_time = time.time()

    for idx, domain in enumerate(domains, 1):
        if idx < START_DOMAIN_INDEX:
            continue

        print(f"\n[Domain {idx}/{total_domains}] Crawling: {domain}")

        start_url = f"https://{domain}"
        urls, status = crawl_domain(start_url, MAX_URLS_PER_DOMAIN)

        if status == "blocked":
            print(f"[SKIPPED] {domain} (IP diblokir)")
            continue

        if status == "rate_limit":
            print(f"[SKIPPED] {domain} (Too Many Requests)")
            continue

        if not urls:
            print(f"[SKIPPED] {domain} (tidak ada internal URL valid)")
            continue

        rows = []
        for i, url in enumerate(urls, 1):
            rows.append({
                "domain_index": idx,
                "domain": domain,
                "url_index": i,
                "url": url
            })

        pd.DataFrame(rows).to_csv(
            OUTPUT_CSV,
            mode="a",
            index=False,
            header=not os.path.exists(OUTPUT_CSV)
        )

    total_elapsed = time.time() - global_start_time
    print("\nDONE")
    print(f"Output: {OUTPUT_CSV}")
    print(f"Total waktu: {total_elapsed/60:.2f} menit")
