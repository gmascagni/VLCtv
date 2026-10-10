import sys
import os
import urllib.parse
import base64
import subprocess

def clean_url(raw):
    if not raw:
        return ""
    
    # Strip quotes
    raw = raw.strip('"\'')
    
    # Strip vlc:// or vlc:
    if raw.startswith("vlc://"):
        raw = raw[6:]
    elif raw.startswith("vlc:"):
        raw = raw[4:]
        
    # Strip trailing slash added by some browsers
    if raw.endswith("/"):
        raw = raw[:-1]
        
    # Check if base64 encoded
    if raw.startswith("b64/"):
        b64_str = raw[4:]
        b64_str += "=" * (-len(b64_str) % 4)
        try:
            return base64.b64decode(b64_str).decode("utf-8")
        except Exception:
            pass

    # URL decode
    unquoted = urllib.parse.unquote(raw)
    
    # Fix stripped colon by browser (e.g. https// -> https://)
    if unquoted.startswith("https//"):
        return "https://" + unquoted[7:]
    elif unquoted.startswith("http//"):
        return "http://" + unquoted[6:]
    elif unquoted.startswith("https/"):
        return "https://" + unquoted[6:]
    elif unquoted.startswith("http/"):
        return "http://" + unquoted[5:]
        
    return unquoted

def main():
    if len(sys.argv) < 2:
        return
        
    raw_arg = " ".join(sys.argv[1:]).strip()
    url = clean_url(raw_arg)
    if not url:
        return

    # Debug log to verify URL received and cleaned
    try:
        log_path = os.path.join(os.environ.get("TEMP", "."), "vlc_launcher.log")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"RAW: {raw_arg}\nCLEAN: {url}\n\n")
    except Exception:
        pass

    # Find VLC
    vlc_candidates = [
        r"C:\Program Files\VideoLAN\VLC\vlc.exe",
        r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
    ]
    vlc_path = None
    for cand in vlc_candidates:
        if os.path.exists(cand):
            vlc_path = cand
            break
            
    if not vlc_path:
        import shutil
        vlc_path = shutil.which("vlc")

    if vlc_path:
        subprocess.Popen(
            [vlc_path, "--network-caching=1500", url],
            creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
            close_fds=True
        )

if __name__ == "__main__":
    main()
