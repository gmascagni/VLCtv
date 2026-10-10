#!/usr/bin/env python3
"""
VLC Channel Guide Generator
Fetches, processes, categorizes, and builds VLC playlists (.m3u8 & .xspf)
and JSON dataset for US-based channels.
"""

import urllib.request
import json
import re
import os
import xml.sax.saxutils as saxutils
from datetime import datetime

US_M3U_URL = "https://iptv-org.github.io/iptv/countries/us.m3u"
CHANNELS_API_URL = "https://iptv-org.github.io/api/channels.json"
FEEDS_API_URL = "https://iptv-org.github.io/api/feeds.json"

CATEGORY_DEFINITIONS = [
    {
        "id": "news",
        "name": "News & Weather",
        "filename": "US_News_Channels",
        "keywords": ["news", "weather", "business", "financial", "c-span", "cheddar", "scripps", 
                     "bloomberg", "cnbc", "msnbc", "cnn", "fox news", "fox weather", "accuweather", 
                     "newsmax", "voa", "law & crime", "court tv", "investigation", "defense tv", "headline"]
    },
    {
        "id": "movies",
        "name": "Movies & Cinema",
        "filename": "US_Movies_Channels",
        "keywords": ["movies", "movie", "cinema", "film", "hollywood", "cinevault", "amc", "classic movies",
                     "retrocrush", "filmrise", "00s replay", "70s cinema", "80s rewind", "90s throwback", 
                     "hallmark movies", "western", "action", "thriller", "horror"]
    },
    {
        "id": "sports",
        "name": "Sports & Outdoors",
        "filename": "US_Sports_Channels",
        "keywords": ["sports", "sport", "espn", "golf", "football", "soccer", "racing", "billiard", 
                     "poker", "wrestling", "mma", "fight", "acc network", "big ten", "stadium", 
                     "motorsport", "darcizzle", "pursuit channel", "auto", "outdoor", "fitness", 
                     "surf", "ski", "skate", "hockey", "baseball", "basketball", "red bull"]
    },
    {
        "id": "entertainment",
        "name": "Entertainment & Series",
        "filename": "US_Entertainment_Channels",
        "keywords": ["entertainment", "series", "comedy", "drama", "reality", "cooking", "travel", 
                     "lifestyle", "food", "afv", "show", "sitcom", "telenovela", "soap", "game show", 
                     "shop", "culture", "relax", "parade", "vevo"]
    },
    {
        "id": "kids",
        "name": "Kids & Family",
        "filename": "US_Kids_Family_Channels",
        "keywords": ["kids", "cartoon", "animation", "anime", "baby shark", "toons", "nickelodeon", 
                     "disney", "hidive", "crunchyroll", "family", "junior"]
    },
    {
        "id": "documentary",
        "name": "Documentary & Science",
        "filename": "US_Documentary_Channels",
        "keywords": ["documentary", "history", "nature", "discovery", "science", "national geographic", 
                     "animal planet", "smithsonian", "wild", "earth", "education", "space", "biography"]
    },
    {
        "id": "music",
        "name": "Music & Radio",
        "filename": "US_Music_Channels",
        "keywords": ["music", "radio", "mtv", "vh1", "stingray", "concert", "country music", 
                     "rock", "hip hop", "jazz", "hits", "soundtrack"]
    },
    {
        "id": "local",
        "name": "Local Broadcast Networks",
        "filename": "US_Local_Broadcast",
        "keywords": ["abc ", "cbs ", "nbc ", "fox ", "pbs ", "cw ", "telemundo ", "univision ", "ion "]
    },
    {
        "id": "public",
        "name": "Public & Government",
        "filename": "US_Public_Government_Channels",
        "keywords": ["legislative", "city council", "accessvision", "public access", "government", 
                     "atxn", "actv", "cmap", "bhtv", "batv"]
    },
    {
        "id": "adult",
        "name": "Adult",
        "filename": "Adult_XXX_Channels",
        "keywords": ["xxx", "adult", "porn", "erotic", "adultiptv"]
    }
]

CUSTOM_CHANNELS = [
    {
        "id": "adultiptv-vod",
        "name": "AdultIPTV.net VOD Videos",
        "category": "Adult",
        "url": "http://adultiptv.net/videos.m3u8",
        "logo": "https://files.adultiptv.net/adultiptvnet.jpg",
        "quality": "HD",
        "network": "AdultIPTV.net",
        "options": [],
        "user_agent": ""
    },
    {
        "id": "adultiptv-livecams",
        "name": "AdultIPTV.net Live Cams",
        "category": "Adult",
        "url": "http://live.adultiptv.net/livecams.m3u8",
        "logo": "https://files.adultiptv.net/adultiptvnet.jpg",
        "quality": "HD",
        "network": "AdultIPTV.net",
        "options": [],
        "user_agent": ""
    },
    {
        "id": "adultiptv-milf",
        "name": "AdultIPTV.net MILF",
        "category": "Adult",
        "url": "http://live.adultiptv.net/milf.m3u8",
        "logo": "https://files.adultiptv.net/adultiptvnet.jpg",
        "quality": "HD",
        "network": "AdultIPTV.net",
        "options": [],
        "user_agent": ""
    },
    {
        "id": "adultiptv-bigdick",
        "name": "AdultIPTV.net Big Dick",
        "category": "Adult",
        "url": "http://live.adultiptv.net/bigdick.m3u8",
        "logo": "https://files.adultiptv.net/adultiptvnet.jpg",
        "quality": "HD",
        "network": "AdultIPTV.net",
        "options": [],
        "user_agent": ""
    },
    {
        "id": "adultiptv-bigtits",
        "name": "AdultIPTV.net Big Tits",
        "category": "Adult",
        "url": "http://live.adultiptv.net/bigtits.m3u8",
        "logo": "https://files.adultiptv.net/adultiptvnet.jpg",
        "quality": "HD",
        "network": "AdultIPTV.net",
        "options": [],
        "user_agent": ""
    },
    {
        "id": "adultiptv-fetish",
        "name": "AdultIPTV.net Fetish",
        "category": "Adult",
        "url": "http://live.adultiptv.net/fetish.m3u8",
        "logo": "https://files.adultiptv.net/adultiptvnet.jpg",
        "quality": "HD",
        "network": "AdultIPTV.net",
        "options": [],
        "user_agent": ""
    },
    {
        "id": "adultiptv-pornstar",
        "name": "AdultIPTV.net Pornstar",
        "category": "Adult",
        "url": "http://live.adultiptv.net/pornstar.m3u8",
        "logo": "https://files.adultiptv.net/adultiptvnet.jpg",
        "quality": "HD",
        "network": "AdultIPTV.net",
        "options": [],
        "user_agent": ""
    },
    {
        "id": "adultiptv-bigass",
        "name": "AdultIPTV.net Big Ass",
        "category": "Adult",
        "url": "http://live.adultiptv.net/bigass.m3u8",
        "logo": "https://files.adultiptv.net/adultiptvnet.jpg",
        "quality": "HD",
        "network": "AdultIPTV.net",
        "options": [],
        "user_agent": ""
    },
    {
        "id": "adultiptv-interracial",
        "name": "AdultIPTV.net Interracial",
        "category": "Adult",
        "url": "http://live.adultiptv.net/interracial.m3u8",
        "logo": "https://files.adultiptv.net/adultiptvnet.jpg",
        "quality": "HD",
        "network": "AdultIPTV.net",
        "options": [],
        "user_agent": ""
    },
    {
        "id": "adultiptv-latina",
        "name": "AdultIPTV.net Latina",
        "category": "Adult",
        "url": "http://live.adultiptv.net/latina.m3u8",
        "logo": "https://files.adultiptv.net/adultiptvnet.jpg",
        "quality": "HD",
        "network": "AdultIPTV.net",
        "options": [],
        "user_agent": ""
    },
    {
        "id": "adultiptv-pov",
        "name": "AdultIPTV.net POV",
        "category": "Adult",
        "url": "http://live.adultiptv.net/pov.m3u8",
        "logo": "https://files.adultiptv.net/adultiptvnet.jpg",
        "quality": "HD",
        "network": "AdultIPTV.net",
        "options": [],
        "user_agent": ""
    },
    {
        "id": "adultiptv-blowjob",
        "name": "AdultIPTV.net Blowjob",
        "category": "Adult",
        "url": "http://live.adultiptv.net/blowjob.m3u8",
        "logo": "https://files.adultiptv.net/adultiptvnet.jpg",
        "quality": "HD",
        "network": "AdultIPTV.net",
        "options": [],
        "user_agent": ""
    },
    {
        "id": "adultiptv-hardcore",
        "name": "AdultIPTV.net Hardcore",
        "category": "Adult",
        "url": "http://live.adultiptv.net/hardcore.m3u8",
        "logo": "https://files.adultiptv.net/adultiptvnet.jpg",
        "quality": "HD",
        "network": "AdultIPTV.net",
        "options": [],
        "user_agent": ""
    },
    {
        "id": "adultiptv-cuckold",
        "name": "AdultIPTV.net Cuckold",
        "category": "Adult",
        "url": "http://live.adultiptv.net/cuckold.m3u8",
        "logo": "https://files.adultiptv.net/adultiptvnet.jpg",
        "quality": "HD",
        "network": "AdultIPTV.net",
        "options": [],
        "user_agent": ""
    },
    {
        "id": "adultiptv-threesome",
        "name": "AdultIPTV.net Threesome",
        "category": "Adult",
        "url": "http://live.adultiptv.net/threesome.m3u8",
        "logo": "https://files.adultiptv.net/adultiptvnet.jpg",
        "quality": "HD",
        "network": "AdultIPTV.net",
        "options": [],
        "user_agent": ""
    },
    {
        "id": "adultiptv-russian",
        "name": "AdultIPTV.net Russian",
        "category": "Adult",
        "url": "http://live.adultiptv.net/russian.m3u8",
        "logo": "https://files.adultiptv.net/adultiptvnet.jpg",
        "quality": "HD",
        "network": "AdultIPTV.net",
        "options": [],
        "user_agent": ""
    },
    {
        "id": "adultiptv-lesbian",
        "name": "AdultIPTV.net Lesbian",
        "category": "Adult",
        "url": "http://live.adultiptv.net/lesbian.m3u8",
        "logo": "https://files.adultiptv.net/adultiptvnet.jpg",
        "quality": "HD",
        "network": "AdultIPTV.net",
        "options": [],
        "user_agent": ""
    },
    {
        "id": "adultiptv-rough",
        "name": "AdultIPTV.net Rough",
        "category": "Adult",
        "url": "http://live.adultiptv.net/rough.m3u8",
        "logo": "https://files.adultiptv.net/adultiptvnet.jpg",
        "quality": "HD",
        "network": "AdultIPTV.net",
        "options": [],
        "user_agent": ""
    },
    {
        "id": "adultiptv-gangbang",
        "name": "AdultIPTV.net Gangbang",
        "category": "Adult",
        "url": "http://live.adultiptv.net/gangbang.m3u8",
        "logo": "https://files.adultiptv.net/adultiptvnet.jpg",
        "quality": "HD",
        "network": "AdultIPTV.net",
        "options": [],
        "user_agent": ""
    },
    {
        "id": "adultiptv-anal",
        "name": "AdultIPTV.net Anal",
        "category": "Adult",
        "url": "http://live.adultiptv.net/anal.m3u8",
        "logo": "https://files.adultiptv.net/adultiptvnet.jpg",
        "quality": "HD",
        "network": "AdultIPTV.net",
        "options": [],
        "user_agent": ""
    },
    {
        "id": "adultiptv-compilation",
        "name": "AdultIPTV.net Compilation",
        "category": "Adult",
        "url": "http://live.adultiptv.net/compilation.m3u8",
        "logo": "https://files.adultiptv.net/adultiptvnet.jpg",
        "quality": "HD",
        "network": "AdultIPTV.net",
        "options": [],
        "user_agent": ""
    },
    {
        "id": "adultiptv-brunette",
        "name": "AdultIPTV.net Brunette",
        "category": "Adult",
        "url": "http://live.adultiptv.net/brunette.m3u8",
        "logo": "https://files.adultiptv.net/adultiptvnet.jpg",
        "quality": "HD",
        "network": "AdultIPTV.net",
        "options": [],
        "user_agent": ""
    },
    {
        "id": "adultiptv-blonde",
        "name": "AdultIPTV.net Blonde",
        "category": "Adult",
        "url": "http://live.adultiptv.net/blonde.m3u8",
        "logo": "https://files.adultiptv.net/adultiptvnet.jpg",
        "quality": "HD",
        "network": "AdultIPTV.net",
        "options": [],
        "user_agent": ""
    },
    {
        "id": "adultiptv-asian",
        "name": "AdultIPTV.net Asian",
        "category": "Adult",
        "url": "http://live.adultiptv.net/asian.m3u8",
        "logo": "https://files.adultiptv.net/adultiptvnet.jpg",
        "quality": "HD",
        "network": "AdultIPTV.net",
        "options": [],
        "user_agent": ""
    },
    {
        "id": "NASA.TV.Public.HD",
        "name": "NASA TV Public (720p HD)",
        "category": "Documentary",
        "url": "https://ntv1.akamaized.net/hls/live/2014075/NASA-NTV1-HLS/master.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/e/e5/NASA_logo.svg",
        "quality": "720p HD",
        "network": "NASA",
        "options": [],
        "user_agent": ""
    },
    {
        "id": "NASA.TV.Media.HD",
        "name": "NASA TV Media (720p HD)",
        "category": "Documentary",
        "url": "https://ntv2.akamaized.net/hls/live/2013923/NASA-NTV2-HLS/master.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/e/e5/NASA_logo.svg",
        "quality": "720p HD",
        "network": "NASA",
        "options": [],
        "user_agent": ""
    }
]

def fetch_data():
    print("Fetching US M3U playlist from iptv-org...")
    req = urllib.request.Request(US_M3U_URL, headers={"User-Agent": "Mozilla/5.0 VLC/3.0.24"})
    with urllib.request.urlopen(req) as resp:
        m3u_text = resp.read().decode("utf-8", errors="ignore")

    print("Fetching channels metadata database...")
    try:
        req_api = urllib.request.Request(CHANNELS_API_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req_api) as resp_api:
            api_channels = json.loads(resp_api.read().decode("utf-8", errors="ignore"))
            api_map = {c["id"]: c for c in api_channels}
    except Exception as e:
        print(f"Warning: could not fetch channels.json ({e}), proceeding with M3U metadata.")
        api_map = {}

    print("Fetching feeds database for language metadata...")
    feeds_map = {}
    try:
        req_feeds = urllib.request.Request(FEEDS_API_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req_feeds) as resp_feeds:
            api_feeds = json.loads(resp_feeds.read().decode("utf-8", errors="ignore"))
            for f in api_feeds:
                cid = f.get("channel")
                fid = f.get("id")
                langs = f.get("languages", [])
                if langs:
                    if cid and fid:
                        feeds_map[f"{cid}@{fid}"] = langs
                    if cid:
                        feeds_map[cid] = langs
    except Exception as e:
        print(f"Warning: could not fetch feeds.json ({e}), proceeding with keyword language detection.")

    return m3u_text, api_map, feeds_map

def build_description(name, category, network=""):
    n_lower = name.lower()
    net_str = f" from {network}" if network else ""
    
    # Specific network/channel patterns
    if "abc news" in n_lower:
        return "24/7 breaking news coverage, live event analysis, and reporting from ABC News."
    if "cbs news" in n_lower:
        return "Live continuous national and global news reporting from CBS News."
    if "bloomberg" in n_lower:
        return "Global business, financial market news, economic updates, and corporate interviews."
    if "cnbc" in n_lower:
        return "Financial market news, real-time stock ticker analysis, and business coverage."
    if "court tv" in n_lower:
        return "Live gavel-to-gavel courtroom trials, legal commentary, and criminal justice journalism."
    if "law & crime" in n_lower:
        return "Live courtroom trials, legal debates, crime investigations, and high-profile verdicts."
    if "accuweather" in n_lower or "weather" in n_lower:
        return "Live meteorological forecasts, real-time radar tracking, and severe weather updates."
    if "cheddar" in n_lower:
        return "Live business news, tech innovations, culture, and market coverage for the digital generation."
    if "c-span" in n_lower:
        return "Gavel-to-gavel U.S. Congressional proceedings, Senate hearings, and public policy forums."
    if "nasa" in n_lower:
        return "Live rocket launches, space station coverage, astronaut missions, and astronomy documentaries."
    if "retrocrush" in n_lower:
        return "Classic golden-age anime series, retro films, and vintage Japanese animation."
    if "00s replay" in n_lower:
        return "Classic television series, reality shows, and pop culture nostalgia from the 2000s."
    if "70s cinema" in n_lower:
        return "Iconic films, cult classics, and cinematic storytelling from the 1970s."
    if "80s rewind" in n_lower:
        return "Favorite 1980s movies, retro blockbusters, and nostalgic cinematic classics."
    if "90s throwback" in n_lower:
        return "Beloved movies and pop culture favorites from the 1990s."
    if "filmrise" in n_lower:
        return f"Acclaimed movies, television series, and genre entertainment{net_str}."
    if "red bull" in n_lower:
        return "Action sports, extreme sports competitions, motorsports, and adventure culture."
    if "stadium" in n_lower:
        return "Live collegiate sports games, studio highlights, insider analysis, and athletics."
    if "golf" in n_lower:
        return "Live golf tournaments, player profiles, instructional lessons, and course tours."
    if "darcizzle" in n_lower or "fishing" in n_lower or "offshore" in n_lower:
        return "Sport fishing adventures, offshore saltwater angling, and boating lifestyle."
    if "car" in n_lower or "auto" in n_lower or "motor" in n_lower or "racing" in n_lower:
        return "Motorsports racing, high-octane automotive builds, and vehicle performance tests."
    if "pursuit channel" in n_lower:
        return "Hunting, fishing, wilderness survival, and outdoor shooting sports."
    if "vevo" in n_lower:
        return "Continuous music video streams featuring chart-topping artists and hits."
    if "stingray" in n_lower:
        return f"Curated music broadcasts and high-fidelity sound tracks{net_str}."
    if "3abn kids" in n_lower:
        return "Faith-based children's animation, Christian stories, and family values."
    if "3abn praise" in n_lower:
        return "Inspirational Christian gospel music, sacred hymns, and worship concerts."
    if "3abn" in n_lower:
        return "Christian programming, health lifestyle seminars, and spiritual ministry broadcasts."
    if "adultiptv" in n_lower or category == "Adult":
        return "Adult entertainment programming and video on-demand streams."
    if n_lower.startswith("abc "):
        return "Local ABC affiliate broadcast featuring regional news, weather, sports, and network programming."
    if n_lower.startswith("cbs "):
        return "Local CBS affiliate broadcast featuring regional news, weather, sports, and network programming."
    if n_lower.startswith("nbc "):
        return "Local NBC affiliate broadcast featuring regional news, weather, sports, and network programming."
    if n_lower.startswith("fox "):
        return "Local FOX affiliate broadcast featuring regional news, weather, sports, and network programming."
    if n_lower.startswith("pbs "):
        return "Public Broadcasting Service affiliate presenting educational, cultural, and community programming."
    if "telemundo" in n_lower:
        return "Spanish-language broadcast network featuring telenovelas, news, sports, and variety shows."
    if "univision" in n_lower:
        return "Spanish-language news, sports, drama, and entertainment broadcasting."
    if "western" in n_lower:
        return "Classic western movies, frontier tales, cowboys, and legendary gunfighter sagas."
    if "horror" in n_lower:
        return "Cult horror films, psychological thrillers, monster classics, and supernatural cinema."
    if "comedy" in n_lower:
        return "Stand-up comedy, hilarious sitcoms, sketch entertainment, and comedy specials."
    if "cooking" in n_lower or "food" in n_lower:
        return "Culinary masters, gourmet recipes, cooking competitions, and delicious dining tours."
    if "anime" in n_lower:
        return "Japanese anime series, animation features, and fan favorites."
    if "nature" in n_lower or "wild" in n_lower or "animal" in n_lower:
        return "Wildlife expeditions, animal adventures, and breathtaking nature documentaries."
    if "history" in n_lower:
        return "Historical documentaries, archaeological explorations, and world history specials."
    if "poker" in n_lower:
        return "Championship poker tournaments, high-stakes cash games, and poker strategy."
    if "fight" in n_lower or "mma" in n_lower or "wrestling" in n_lower or "combat" in n_lower:
        return "Action-packed combat sports, mixed martial arts, professional wrestling, and bout archives."
        
    # Category based defaults
    cat_defaults = {
        "News": f"Live news coverage, breaking headlines, weather forecasts, and current affairs reporting{net_str}.",
        "Movies": f"Feature films, classic cinema, Hollywood entertainment, and genre movies{net_str}.",
        "Sports": f"Live sports events, tournament highlights, athletic competitions, and sports talk{net_str}.",
        "Entertainment": f"Popular television series, comedy, reality entertainment, and lifestyle shows{net_str}.",
        "Kids & Family": f"Animated adventures, family-friendly series, cartoons, and children's entertainment{net_str}.",
        "Documentary": f"Educational documentaries, science explorations, history, and real-world investigations{net_str}.",
        "Music": f"Curated music videos, artist spotlights, concerts, and continuous music streaming{net_str}.",
        "Local Broadcast": "Regional broadcast television featuring local community news, weather, and syndicated programming.",
        "Public & Government": "Public access programming, municipal council meetings, and civic government coverage.",
        "Adult": "Adult entertainment programming and adult video streams.",
        "General & Regional": f"Community television, regional broadcasts, and general entertainment programming{net_str}."
    }
    return cat_defaults.get(category, f"Live stream broadcast featuring {category} programming{net_str}.")

def parse_m3u(m3u_text, api_map, feeds_map):
    lines = m3u_text.splitlines()
    channels = []
    cur_item = {}

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("#EXTINF:"):
            cur_item = {"raw_extinf": line, "options": []}
            tvg_id = re.search(r'tvg-id="([^"]*)"', line)
            tvg_logo = re.search(r'tvg-logo="([^"]*)"', line)
            group_title = re.search(r'group-title="([^"]*)"', line)
            user_agent = re.search(r'http-user-agent="([^"]*)"', line)
            name = line.split(",", 1)[1] if "," in line else "Unknown Channel"

            cur_item["id"] = tvg_id.group(1) if tvg_id else ""
            cur_item["logo"] = tvg_logo.group(1) if tvg_logo else ""
            cur_item["group"] = group_title.group(1) if group_title else "General"
            cur_item["user_agent"] = user_agent.group(1) if user_agent else ""
            cur_item["name"] = name.strip()
        elif line.startswith("#EXTVLCOPT:"):
            if "options" in cur_item:
                cur_item["options"].append(line)
        elif not line.startswith("#"):
            if cur_item:
                cur_item["url"] = line
                channels.append(cur_item)
                cur_item = {}

    # Post-process & categorize
    processed = []
    for ch in channels:
        name_l = ch["name"].lower()
        group_l = ch["group"].lower()
        api_data = api_map.get(ch["id"], {})
        api_cats = [c.lower() for c in api_data.get("categories", [])]
        raw_cats = [c.strip().lower() for c in group_l.split(";") if c.strip()]
        combined_meta = set(raw_cats) | set(api_cats)

        # Resolution detection
        quality = "SD"
        if "1080p" in name_l or "fhd" in name_l:
            quality = "1080p FHD"
        elif "720p" in name_l or "hd" in name_l:
            quality = "720p HD"
        elif "480p" in name_l:
            quality = "480p SD"
        elif "360p" in name_l:
            quality = "360p SD"

        # Categorization logic
        assigned_cat = "General & Regional"
        
        # 1. News
        if any(k in combined_meta for k in ["news", "weather", "business"]) or \
           any(k in name_l for k in ["news", "weather", "bloomberg", "cnbc", "msnbc", "cnn", "cheddar", "scripps", "newsmax", "law & crime", "court tv"]):
            assigned_cat = "News"
        # 2. Sports
        elif any(k in combined_meta for k in ["sports", "outdoor", "auto", "fitness", "racing"]) or \
             any(k in name_l for k in ["sports", "sport", "espn", "golf", "football", "soccer", "racing", "billiard", "poker", "wrestling", "mma", "fight", "acc network", "big ten", "stadium", "motorsport", "darcizzle", "pursuit channel"]):
            assigned_cat = "Sports"
        # 3. Movies
        elif any(k in combined_meta for k in ["movies", "classic", "cinema", "film"]) or \
             any(k in name_l for k in ["movie", "movies", "cinema", "film", "cinevault", "amc", "retrocrush", "filmrise", "00s replay", "70s cinema", "80s rewind", "90s throwback", "hallmark"]):
            assigned_cat = "Movies"
        # 4. Kids
        elif any(k in combined_meta for k in ["kids", "animation", "family"]) or \
             any(k in name_l for k in ["kids", "cartoon", "animation", "anime", "baby shark", "toons", "nickelodeon", "disney", "hidive", "crunchyroll"]):
            assigned_cat = "Kids & Family"
        # 5. Documentary
        elif any(k in combined_meta for k in ["documentary", "education", "science"]) or \
             any(k in name_l for k in ["documentary", "history", "nature", "discovery", "science", "national geographic", "animal planet", "smithsonian", "wild"]):
            assigned_cat = "Documentary"
        # 6. Music
        elif "music" in combined_meta or any(k in name_l for k in ["music", "radio", "mtv", "vh1", "vevo", "stingray", "concert", "praise him music network"]):
            assigned_cat = "Music"
        # 7. Local Broadcast
        elif any(name_l.startswith(p) for p in ["abc ", "cbs ", "nbc ", "fox ", "pbs ", "cw ", "telemundo ", "univision ", "ion "]):
            assigned_cat = "Local Broadcast"
        # 8. Legislative & Public
        elif "legislative" in combined_meta or any(k in name_l for k in ["legislative", "city council", "accessvision", "public access", "government", "atxn"]):
            assigned_cat = "Public & Government"
        # 9. Entertainment
        elif any(k in combined_meta for k in ["entertainment", "series", "comedy", "lifestyle", "cooking", "travel", "shop", "relax", "culture"]) or \
             any(k in name_l for k in ["entertainment", "comedy", "series", "drama", "reality", "cooking", "travel", "food", "afv", "show"]):
            assigned_cat = "Entertainment"

        clean_name = ch["name"]
        network = api_data.get("network") or ""
        desc = build_description(clean_name, assigned_cat, network)

        # Language detection
        ch_langs = feeds_map.get(ch["id"]) or feeds_map.get(ch["id"].split("@")[0]) or []
        if not ch_langs:
            if any(w in name_l for w in ["spanish", "español", "latino", "telemundo", "univision", "unimás", "estrella", "telexitos"]):
                ch_langs = ["spa"]
            elif any(w in name_l for w in ["french", "français"]):
                ch_langs = ["fra"]
            elif "arabic" in name_l:
                ch_langs = ["ara"]
            elif "russian" in name_l:
                ch_langs = ["rus"]
            elif "chinese" in name_l:
                ch_langs = ["zho"]
            elif "korean" in name_l:
                ch_langs = ["kor"]
            elif "vietnamese" in name_l:
                ch_langs = ["vie"]
            else:
                ch_langs = ["eng"]

        primary_lang = ch_langs[0] if ch_langs else "eng"

        processed.append({
            "id": ch["id"],
            "name": clean_name,
            "category": assigned_cat,
            "description": desc,
            "languages": ch_langs,
            "primary_lang": primary_lang,
            "url": ch["url"],
            "logo": ch["logo"],
            "quality": quality,
            "network": network,
            "options": ch["options"],
            "user_agent": ch["user_agent"]
        })

    for custom_ch in CUSTOM_CHANNELS:
        if not custom_ch.get("description"):
            custom_ch["description"] = build_description(custom_ch["name"], custom_ch["category"], custom_ch.get("network", ""))
        custom_ch["languages"] = ["eng"]
        custom_ch["primary_lang"] = "eng"
    processed.extend(CUSTOM_CHANNELS)
    return processed

def write_m3u8(filepath, playlist_title, channels):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write('#EXTM3U x-tvg-url="https://iptv-org.github.io/epg/guides/us.xml"\n')
        for ch in channels:
            # Build attributes
            attrs = ['#EXTINF:-1']
            if ch["id"]:
                attrs.append(f'tvg-id="{ch["id"]}"')
            attrs.append(f'tvg-name="{ch["name"]}"')
            if ch["logo"]:
                attrs.append(f'tvg-logo="{ch["logo"]}"')
            attrs.append(f'group-title="{ch["category"]}"')
            
            f.write(f'{" ".join(attrs)},{ch["name"]}\n')
            f.write(f'#EXTGRP:{ch["category"]}\n')
            if ch.get("description"):
                f.write(f'#EXTREM:Description: {ch["description"]}\n')
            
            # VLC options
            if ch["user_agent"]:
                f.write(f'#EXTVLCOPT:http-user-agent={ch["user_agent"]}\n')
            # Add network caching for smooth VLC streaming
            f.write('#EXTVLCOPT:network-caching=1500\n')
            for opt in ch["options"]:
                if "http-user-agent" not in opt and "network-caching" not in opt:
                    f.write(f'{opt}\n')
            f.write(f'{ch["url"]}\n')

def write_xspf(filepath, playlist_title, channels):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<playlist version="1" xmlns="http://xspf.org/ns/0/" xmlns:vlc="http://www.videolan.org/vlc/playlist/ns/0/">\n')
        f.write(f'  <title>{saxutils.escape(playlist_title)}</title>\n')
        f.write('  <trackList>\n')
        for i, ch in enumerate(channels):
            f.write('    <track>\n')
            f.write(f'      <location>{saxutils.escape(ch["url"])}</location>\n')
            f.write(f'      <title>{saxutils.escape(ch["name"])}</title>\n')
            if ch["logo"]:
                f.write(f'      <image>{saxutils.escape(ch["logo"])}</image>\n')
            ann = ch.get("description") or ch["category"]
            f.write(f'      <annotation>{saxutils.escape(ann)}</annotation>\n')
            f.write('      <extension application="http://www.videolan.org/vlc/playlist/0">\n')
            f.write(f'        <vlc:id>{i}</vlc:id>\n')
            f.write('        <vlc:option>network-caching=1500</vlc:option>\n')
            if ch["user_agent"]:
                f.write(f'        <vlc:option>http-user-agent={saxutils.escape(ch["user_agent"])}</vlc:option>\n')
            f.write('      </extension>\n')
            f.write('    </track>\n')
        f.write('  </trackList>\n')
        f.write('</playlist>\n')

def main():
    print("=== VLC Channel Guide Builder ===")
    m3u_text, api_map, feeds_map = fetch_data()
    channels = parse_m3u(m3u_text, api_map, feeds_map)
    print(f"Successfully processed {len(channels)} US channels.")

    output_dir = os.path.dirname(os.path.abspath(__file__))

    # 1. Generate Master All Channels playlist
    all_m3u8 = os.path.join(output_dir, "US_All_Channels.m3u8")
    all_xspf = os.path.join(output_dir, "US_All_Channels.xspf")
    print(f"Writing master playlist: {all_m3u8}")
    write_m3u8(all_m3u8, "All US TV Channels - Complete Guide", channels)
    print(f"Writing master XSPF: {all_xspf}")
    write_xspf(all_xspf, "All US TV Channels - Complete Guide", channels)

    # 2. Generate Category playlists
    cat_counts = {}
    lang_counts = {}
    for ch in channels:
        cat_counts[ch["category"]] = cat_counts.get(ch["category"], 0) + 1
        pl = ch.get("primary_lang", "eng")
        lang_counts[pl] = lang_counts.get(pl, 0) + 1

    for cat_def in CATEGORY_DEFINITIONS:
        cat_name = cat_def["name"]
        cat_id = cat_def["id"]
        filename_base = cat_def["filename"]

        # Match channels:
        # News matches 'News', Movies matches 'Movies', Sports matches 'Sports', etc.
        matched = []
        if cat_id == "news":
            matched = [c for c in channels if c["category"] == "News"]
        elif cat_id == "movies":
            matched = [c for c in channels if c["category"] == "Movies"]
        elif cat_id == "sports":
            matched = [c for c in channels if c["category"] == "Sports"]
        elif cat_id == "entertainment":
            matched = [c for c in channels if c["category"] == "Entertainment"]
        elif cat_id == "kids":
            matched = [c for c in channels if c["category"] == "Kids & Family"]
        elif cat_id == "documentary":
            matched = [c for c in channels if c["category"] == "Documentary"]
        elif cat_id == "music":
            matched = [c for c in channels if c["category"] == "Music"]
        elif cat_id == "local":
            matched = [c for c in channels if c["category"] == "Local Broadcast"]
        elif cat_id == "public":
            matched = [c for c in channels if c["category"] == "Public & Government"]
        elif cat_id == "adult":
            matched = [c for c in channels if c["category"] == "Adult"]

        if matched:
            m3u8_path = os.path.join(output_dir, f"{filename_base}.m3u8")
            xspf_path = os.path.join(output_dir, f"{filename_base}.xspf")
            print(f"Generating {cat_name} ({len(matched)} channels) -> {filename_base}.m3u8")
            write_m3u8(m3u8_path, f"US {cat_name} Channels", matched)
            write_xspf(xspf_path, f"US {cat_name} Channels", matched)

    # 3. Export JSON data for the interactive HTML Channel Guide
    json_path = os.path.join(output_dir, "channels_data.json")
    print(f"Writing JSON dataset: {json_path}")
    data_payload = {
        "generated_at": datetime.now().isoformat(),
        "total_count": len(channels),
        "categories": cat_counts,
        "languages": lang_counts,
        "channels": [
            {
                "id": c["id"],
                "name": c["name"],
                "category": c["category"],
                "url": c["url"],
                "logo": c["logo"],
                "quality": c["quality"],
                "network": c["network"],
                "description": c.get("description", ""),
                "languages": c.get("languages", ["eng"]),
                "primary_lang": c.get("primary_lang", "eng")
            }
            for c in channels
        ]
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data_payload, f, indent=2)

    js_path = os.path.join(output_dir, "channels_data.js")
    print(f"Writing JavaScript dataset: {js_path}")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write("window.CHANNELS_DATA = " + json.dumps(data_payload) + ";\n")

    def make_launcher(filename, title, playlist_file):
        safe_title = title.replace("&", "and")
        batch_content = (
            '@echo off\n'
            f'echo Launching {safe_title} in VLC Media Player...\n'
            'set "VLC=C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"\n'
            'if not exist "%VLC%" set "VLC=C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"\n'
            'if not exist "%VLC%" (\n'
            f'    start "" "%~dp0{playlist_file}"\n'
            ') else (\n'
            f'    start "" "%VLC%" "%~dp0{playlist_file}"\n'
            ')\n'
        )
        with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
            f.write(batch_content)

    make_launcher("Open_All_In_VLC.bat", "All US Channels", "US_All_Channels.m3u8")
    make_launcher("Open_News_In_VLC.bat", "US News Channels", "US_News_Channels.m3u8")
    make_launcher("Open_Movies_In_VLC.bat", "US Movies Channels", "US_Movies_Channels.m3u8")
    make_launcher("Open_Sports_In_VLC.bat", "US Sports Channels", "US_Sports_Channels.m3u8")
    make_launcher("Open_Adult_In_VLC.bat", "Adult Channels", "Adult_XXX_Channels.m3u8")

    # Launch Web Guide
    with open(os.path.join(output_dir, "Launch_Channel_Guide.bat"), "w", encoding="utf-8") as f:
        f.write('@echo off\n')
        f.write('echo Launching Interactive VLC Channel Guide in your web browser...\n')
        f.write('start "" "%~dp0index.html"\n')

    print("\n=== All VLC Playlists and Launchers Generated Successfully! ===")
    print("Summary:")
    for cat, count in sorted(cat_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {cat}: {count} channels")
    print(f"Total: {len(channels)} channels.")

if __name__ == "__main__":
    main()
