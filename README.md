# 📺 VLC US Channel Guide

A complete, high-performance **VLC Media Player Channel Guide** featuring **1,493 free, legal, and publicly broadcast US TV channels**, categorized by **News & Weather**, **Documentary & Science (including NASA TV)**, **Movies**, **Sports**, **Entertainment**, **Kids**, **Local Broadcast**, and **All US Channels**.

Styled with **Brushed Aluminum Bezels, Embossed Metallic Rows & Cards**, and subtle **Watermark Channel Logos**.

Features a **Traditional Cable TV Linear Row Guide (EPG)** layout with channel numbers (`CH 001`), network logo badges, pulsing live broadcast indicators, and 1-click toggling back to Card Grid view.

---

## 🌐 Live Web Guide on GitHub Pages

You can host and access this channel guide from anywhere in the world on your phone, tablet, or laptop:

1. In your GitHub repository (`https://github.com/gmascagni/VLCtv`):
   - Go to **Settings** &rarr; **Pages** (under "Code and automation").
   - Under **Build and deployment** &rarr; **Branch**, select `main` and folder `/(root)`.
   - Click **Save**.
2. Your channel guide will be live at:
   - **`https://gmascagni.github.io/VLCtv/`**

---

## 🚀 Quick Start (One-Click Launchers)

Double-click any of the provided Windows `.bat` launchers in this folder to open your desired category directly in VLC:

| Launcher File | Description | Channels |
| :--- | :--- | :--- |
| **`Enable_VLC_OneClick.bat`** | **Run once** to enable 1-click "Open in VLC" buttons in your browser | *Setup* |
| **`Open_All_In_VLC.bat`** | Opens **All US Channels** in VLC with category folders | **1,493** |
| **`Open_News_In_VLC.bat`** | Opens **News, Financial, Weather & Emergency Channels** | **118** |
| **`Open_Movies_In_VLC.bat`** | Opens **Movies & Cinema Channels** | **139** |
| **`Open_Sports_In_VLC.bat`** | Opens **Sports, Racing & Outdoor Channels** | **89** |
| **`Open_Adult_In_VLC.bat`** | Opens **Adult Live Channels** | **24** |
| **`Launch_Channel_Guide.bat`** | Launches the **Interactive Web TV Guide** in your browser | **1,493** |

---

## 🚗 Portable Road Trip Application (`VLC_Channel_Guide_Portable.zip`)

For travel and road trips, everything needed to filter and launch all 1,493 channels is packaged into a self-contained portable bundle:
* **Direct Launcher**: Double-click `Launch_Channel_Guide.bat` on any laptop or Windows tablet.
* **100% In-Browser Filtering**: Filter by any category, resolution, or language without needing separate files.
* **Cable TV Guide Layout**: Familiar linear guide row view with channel numbers (`CH 001`), station logos, and live feeds.
* **Zero Installation**: Unzip anywhere (e.g. on a USB thumb drive or laptop desktop) and launch.

---

## 📁 Included Playlist Files

Both standard **M3U8** (with extended EPG and VLC tags) and native **XSPF** (XML Shareable Playlist Format for VLC) playlists are included:

### 1. Main Requested Playlists
- **`US_All_Channels.m3u8`** & **`US_All_Channels.xspf`**
  - Complete guide with all 1,493 channels.
  - Tagged with `#EXTGRP` so VLC organizes channels into collapsible category folders in the playlist sidebar.
- **`US_News_Channels.m3u8`** & **`US_News_Channels.xspf`**
  - 118 News channels (ABC News Live, CBS News, Bloomberg Originals, Cheddar, Newsmax, Law & Crime, Court TV, Scripps News, Weather Channel / Fox Weather, etc.).
- **`US_Movies_Channels.m3u8`** & **`US_Movies_Channels.xspf`**
  - 139 Movie channels (AMC, 00s Replay, 24 Hour Free Movies, FilmRise Western, Cinevault, 70s Cinema, 80s Rewind, 90s Throwback, RetroCrush, Hallmark, etc.).
- **`US_Sports_Channels.m3u8`** & **`US_Sports_Channels.xspf`**
  - 89 Sports channels (ACC Network, Big Ten Network, beIN SPORTS XTRA, Fubo Sports, Red Bull TV, Fight Network, World Poker Tour, Stadium, Golf Kingdom, Pursuit Channel, etc.).
- **`Adult_XXX_Channels.m3u8`** & **`Adult_XXX_Channels.xspf`**
  - 24 Adult channels (Passcode protected with `xxx` on web guide).

### 2. Additional Curated Categories
- **`US_Entertainment_Channels.m3u8`** & **`.xspf`** (297 channels — Comedy, Drama, Reality, Cooking, Lifestyle)
- **`US_Kids_Family_Channels.m3u8`** & **`.xspf`** (85 channels — Animation, Cartoons, Anime, Family)
- **`US_Documentary_Channels.m3u8`** & **`.xspf`** (95 channels — NASA TV feeds, History, Wildlife, Science, Nature, Smithsonian)
- **`US_Music_Channels.m3u8`** & **`.xspf`** (72 channels — MTV feeds, Vevo, Country, Rock, Live Concerts)
- **`US_Local_Broadcast.m3u8`** & **`.xspf`** (116 channels — Network affiliates across the US: ABC, CBS, NBC, FOX, PBS)
- **`US_Public_Government_Channels.m3u8`** & **`.xspf`** (99 channels — C-SPAN style, City Council, State Legislature)
- **`US_Religious_Channels.m3u8`** & **`.xspf`** (114 channels — Faith & Religious broadcasting)

---

## 📺 Interactive Web Channel Guide (`index.html`)

An interactive TV Guide web application is included in this folder:
- **Cable TV Guide Rows & Card Grid**: Defaults to a clean Cable TV row guide with station numbers, logos, and program summaries. Swap back to Card Grid with a single click anytime.
- **Instant Search**: Search by channel call sign, name, network, category, or keywords in descriptions.
- **Channel Synopsis on Every Row**: Clear, concise descriptions of each channel's programming format, genres, and parent network.
- **Real-Time "Now Playing" Program Guide**: Clicking **Watch** opens the live player with a live schedule inspector:
  - **Live FAST/Pluto Channels**: Shows real-time current program titles, episode names, full program synopses, air times, and a live progress bar.
  - **Live Web/Independent Streams**: Shows broadcast genre format and instructions to view EPG in VLC.
- **Passcode-Protected Adult Section**: Unlocks with password `xxx`.
- **Category Filter Pills**: Switch between All, News, Movies, Sports, Entertainment, etc., with a single click.
- **In-Browser Live Stream Preview**: Powered by an embedded HLS video player to test or watch streams before opening VLC.
- **Milled Brushed Aluminum Theme**: Heavy metallic bezels, tactile embossed cards, and watermark station logos.
- **One-Click Actions**:
  - `Watch` — Watch stream and inspect current show schedule in browser.
  - `VLC` — 1-click launch directly in VLC Media Player (with protocol handler or automatic playlist download).
  - `📋 Copy` — Copies the direct `.m3u8` stream URL for quick pasting into VLC (`Ctrl+N`).
- **Direct Downloads**: Download individual or master playlists directly from the header.

To open the web guide, double-click **`Launch_Channel_Guide.bat`** or double-click **`index.html`**.

---

## 🛠️ How to View & Organize Channels in VLC

### Step 1: Open the Playlist
- Drag and drop `US_All_Channels.m3u8` into VLC.
- Or press `Ctrl + O` in VLC, select `US_All_Channels.m3u8`, and click **Open**.

### Step 2: Open Playlist View
- Press **`Ctrl + L`** to show the Playlist window.

### Step 3: Enable Collapsible Category Folders
- In VLC, right-click inside the Playlist window or click **View** > **Playlist View Mode**.
- Select **Tree** or **Grouped by Category**.
- Channels will be neatly sorted into collapsible groups: **News**, **Movies**, **Sports**, **Entertainment**, etc.

### Step 4: Stream Buffering Optimization (Recommended)
IPTV streams benefit from a 1.5–2 second network cache buffer for stutter-free playback:
1. In VLC, go to **Tools** > **Preferences** (`Ctrl + P`).
2. At the bottom left under *Show settings*, select **All**.
3. In the left panel, click on **Input / Codecs**.
4. Scroll down on the right to the **Advanced** section.
5. Set **Network caching (ms)** to `1500` or `2000`.
6. Click **Save**.

*(Note: The generated M3U8 files also include `#EXTVLCOPT:network-caching=1500` per channel).*

### Step 5: Subtitles & English Translation
- **Cycle Subtitles in VLC**: Press **`V`** to cycle through embedded Closed Captions / Subtitles (or turn them off).
- **Secondary Audio / SAP Dubbing**: Press **`B`** to cycle available audio tracks (e.g. switch from foreign audio to English SAP commentary).
- **Real-Time Live Translation**: Use Google Chrome or Microsoft Edge's on-device AI Live Translate feature (`chrome://settings/accessibility` > Live Caption > Live Translate to English) to automatically transcribe foreign speech and display real-time English subtitles on your screen!

### Step 6: View Channel Descriptions & Program Guides in VLC
- **View Channel Synopsis**: Press **`Ctrl + I`** (*Current Media Information*) on any playing stream to view its genre and full description embedded in the XSPF `<annotation>` tags.
- **View Program Guide (EPG)**: Press **`Shift + G`** or select **Tools** > **Program Guide** to open VLC's TV schedule grid window showing currently playing and upcoming shows!

---

## ⌨️ VLC Channel Surfing Shortcuts

| Key | Action |
| :--- | :--- |
| **`Space`** | Play / Pause |
| **`N`** | Next Channel in list |
| **`P`** | Previous Channel in list |
| **`V`** | **Cycle Subtitles / Closed Captions [CC]** |
| **`B`** | **Cycle Audio Tracks (SAP / English Dubbing)** |
| **`F`** | Toggle Fullscreen |
| **`Ctrl + L`** | Toggle Playlist View |
| **`Ctrl + N`** | Open Network Stream dialog (paste copied stream URL) |
| **`Ctrl + Up` / `Ctrl + Down`** | Volume Up / Down |
| **`M`** | Mute Audio |

---

## 🔄 Updating Channels in the Future

Channel stream URLs are maintained by the open-source IPTV community and occasionally update. You can refresh and regenerate all playlists at any time:

1. Open PowerShell or Command Prompt in this folder.
2. Run:
   ```cmd
   python generate_channel_guide.py
   ```
3. The script will automatically download the latest streams, categorize them, and update all `.m3u8`, `.xspf`, `.bat`, and web guide data files.

---

## ⚖️ Legal & Copyright Information
All streams listed in this guide are publicly available, free-to-air broadcast feeds provided openly by copyright owners, television networks, and public access broadcasters without paywall or authentication.
