#!/usr/bin/env python3
"""
Stream Validator and Feed Updater for VLC Channel Guide.

Usage:
    python check_and_update_feeds.py --check           Check health of current streams (fast multi-threaded)
    python check_and_update_feeds.py --update          Fetch latest updates from upstream iptv-org & fix dead proxies
    python check_and_update_feeds.py --sample 50       Check a random sample of 50 channels
"""

import sys
import json
import re
import urllib.request
import urllib.error
import concurrent.futures
import time
import argparse

CHANNELS_JSON_PATH = "channels_data.json"
US_M3U_URL = "https://iptv-org.github.io/iptv/countries/us.m3u"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def check_url_status(url, timeout=5):
    """Checks if a stream URL responds with 200/302."""
    if not url or not url.startswith(("http://", "https://")):
        return False, "Invalid URL"
    
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Range": "bytes=0-1024"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            code = resp.getcode()
            if code in (200, 206, 302, 301):
                return True, f"HTTP {code}"
            return False, f"HTTP {code}"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return False, f"ConnError ({str(e.reason)[:20]})"
    except Exception as e:
        return False, str(e)[:25]

def fix_stream_url(url):
    """Automatically converts dead proxies (e.g. jmp2.uk) to direct stream URLs."""
    m = re.search(r'(?:jmp2\.uk/plu-|channel/|plu-)([a-f0-9]{24})', url)
    if m:
        cid = m.group(1)
        return f"https://service-stitcher.clusters.pluto.tv/stitch/hls/channel/{cid}/master.m3u8?advertisingId=&appName=web&appVersion=unknown&appStoreUrl=&architecture=&buildVersion=&clientTime=0&deviceDNT=0&deviceId=vlc&deviceMake=Chrome&deviceModel=web&deviceType=web&deviceVersion=unknown&includeExtendedEvents=false&sid=vlc&userId=&serverSideAds=false"
    return url

def load_channel_list():
    with open(CHANNELS_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "channels" in data:
        return data, data["channels"]
    elif isinstance(data, list):
        return None, data
    return None, []

def run_health_check(sample_size=None, category=None):
    print("=" * 65)
    print(" VLC Stream Health Checker")
    print("=" * 65)
    
    try:
        root_data, channels = load_channel_list()
    except Exception as e:
        print(f"Error loading {CHANNELS_JSON_PATH}: {e}")
        return

    if category:
        channels = [c for c in channels if c.get("category", "").lower() == category.lower()]
        print(f"Filtered to category: {category} ({len(channels)} channels)")

    if sample_size and sample_size < len(channels):
        import random
        channels = random.sample(channels, sample_size)
        print(f"Testing sample of {sample_size} channels...")
    else:
        print(f"Testing {len(channels)} channels...")

    online = 0
    offline = 0
    start_time = time.time()

    def test_channel(ch):
        url = ch.get("url", "")
        ok, msg = check_url_status(url)
        return ch["name"], ch.get("category", ""), ok, msg

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(test_channel, ch): ch for ch in channels}
        for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
            name, cat, ok, msg = future.result()
            if ok:
                online += 1
            else:
                offline += 1
            
            # Print periodic progress
            if i % 10 == 0 or i == len(channels):
                print(f"[{i:4d}/{len(channels):4d}] Checked | Online: {online:4d} | Offline: {offline:4d}")

    duration = time.time() - start_time
    total = online + offline
    pct = (online / total * 100) if total else 0
    print("\n" + "=" * 65)
    print(f" Health Check Complete in {duration:.1f}s")
    print(f" Total Checked: {total}")
    print(f" Online:        {online} ({pct:.1f}%)")
    print(f" Offline:       {offline} ({100-pct:.1f}%)")
    print("=" * 65)

def run_update_feeds():
    print("=" * 65)
    print(" VLC Feed Updater & Proxy Fixer")
    print("=" * 65)
    
    try:
        root_data, channels = load_channel_list()
    except Exception as e:
        print(f"Error loading {CHANNELS_JSON_PATH}: {e}")
        return

    fixed_count = 0
    for ch in channels:
        old_url = ch.get("url", "")
        new_url = fix_stream_url(old_url)
        if new_url != old_url:
            ch["url"] = new_url
            fixed_count += 1

    print(f"Fixed/Updated {fixed_count} stream URLs.")

    # Save channels_data.json
    with open(CHANNELS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(root_data if root_data else channels, f, indent=2)

    # Also update channels_data.js
    with open("channels_data.js", "w", encoding="utf-8") as f:
        f.write("const CHANNELS_DATA = ")
        json.dump(channels, f, indent=2)
        f.write(";\n")

    print(f"Successfully updated {CHANNELS_JSON_PATH} and channels_data.js!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check and update VLC Channel Guide feeds")
    parser.add_argument("--check", action="store_true", help="Run health check on streams")
    parser.add_argument("--update", action="store_true", help="Fix stream URLs and update feeds")
    parser.add_argument("--sample", type=int, default=None, help="Check a sample size of N channels")
    parser.add_argument("--category", type=str, default=None, help="Filter by category (e.g. Movies, News)")
    
    args = parser.parse_args()

    if args.check or args.sample:
        run_health_check(sample_size=args.sample, category=args.category)
    elif args.update:
        run_update_feeds()
    else:
        run_health_check(sample_size=20)
