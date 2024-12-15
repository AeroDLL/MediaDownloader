import os
import sys
import time
from colorama import init, Fore, Style
import yt_dlp

# Renkleri Başlat
init(autoreset=True)

# --- AYARLAR ---
DOWNLOAD_FOLDER = "MediaRipper_Downloads"
LANG = 'EN' # Varsayılan (Default)

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# --- DİL SÖZLÜĞÜ (TRANSLATION DICTIONARY) ---
TEXTS = {
    'TR': {
        'select_lang': " [?] Dil Seçiniz / Select Language:",
        'supported': "    [+] Desteklenen: YouTube, Instagram, TikTok, X, Twitch",
        'downloading': "    [>>] İndiriliyor",
        'speed': "Hız",
        'success': "    [V] İndirme tamamlandı! İşleniyor...",
        'video_mode': " [*] Ultra Video Modu Aktif (Video+Ses)...",
        'audio_mode': " [*] Ses Modu Aktif (MP3 - 192kbps)...",
        'analyzing': " [!] Hedef Taranıyor...",
        'target': " [Hedef]",
        'source': " [Kaynak]",
        'ok_msg': " [OK] Dosya Kaydedildi:",
        'error_msg': " [X] HATA:",
        'hint_ffmpeg': " İpucu: FFmpeg yüklü mü? Link doğru mu?",
        'continue': " Devam etmek için Enter...",
        'menu_1': "  [1] ⚔️  Video İndir (Max Kalite / 4K)",
        'menu_2': "  [2] 🎵  Müzik İndir (MP3 Dönüştür)",
        'menu_3': "  [3] 📦  Playlist İndir (Toplu İndirme)",
        'menu_4': "  [4] 💀  Çıkış (Exit)",
        'choice': "  Komut (1-4): ",
        'paste_link': "  URL Yapıştır: ",
        'playlist_link': "  Playlist URL: ",
        'playlist_warn': "  [!] Uyarı: Tüm liste indirilecek, zaman alabilir.",
        'confirm': "  Onaylıyor musun? (e/h): ",
        'unknown': "Bilinmeyen Dosya"
    },
    'EN': {
        'select_lang': " [?] Select Language / Dil Seçiniz:",
        'supported': "    [+] Supported: YouTube, Instagram, TikTok, X, Twitch",
        'downloading': "    [>>] Downloading",
        'speed': "Speed",
        'success': "    [V] Download complete! Processing...",
        'video_mode': " [*] Ultra Video Mode Active (Video+Audio)...",
        'audio_mode': " [*] Audio Mode Active (MP3 - 192kbps)...",
        'analyzing': " [!] Scanning Target...",
        'target': " [Target]",
        'source': " [Source]",
        'ok_msg': " [OK] File Saved:",
        'error_msg': " [X] ERROR:",
        'hint_ffmpeg': " Hint: Is FFmpeg installed? Is the link correct?",
        'continue': " Press Enter to continue...",
        'menu_1': "  [1] ⚔️  Download Video (Max Quality / 4K)",
        'menu_2': "  [2] 🎵  Download Audio (Convert to MP3)",
        'menu_3': "  [3] 📦  Download Playlist (Bulk)",
        'menu_4': "  [4] 💀  Exit",
        'choice': "  Command (1-4): ",
        'paste_link': "  Paste URL: ",
        'playlist_link': "  Playlist URL: ",
        'playlist_warn': "  [!] Warning: Bulk download may take time.",
        'confirm': "  Confirm? (y/n): ",
        'unknown': "Unknown File"
    }
}

# --- YARDIMCI FONKSIYONLAR ---
def t(key):
    return TEXTS[LANG].get(key, "???")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def title(text):
    os.system(f'title MediaRipper by AeroDLL | {text}')

def select_language():
    global LANG
    clear()
    # Dil seçimi için basit ve şık bir logo
    print(Fore.RED + Style.BRIGHT + """
    [ MediaRipper System Boot ]
    """)
    print(Fore.WHITE + "   [1] English")
    print(Fore.WHITE + "   [2] Türkçe")
    
    c = input(Fore.RED + "\n   >> ")
    if c == '2':
        LANG = 'TR'
    else:
        LANG = 'EN'

def banner():
    clear()
    # AERO'ya Özel Tasarım Logo
    print(Fore.RED + Style.BRIGHT + r"""
  __  __          _ _       _____  _
 |  \/  |___   __| (_) __ _|  __ \(_)
 | |\/| / _ \ / _` | |/ _` | |__) | |_ __  _ __   ___ _ __
 | |  | |  __/| (_| | | (_| |  _  /| | '_ \| '_ \ / _ \ '__|
 |_|  |_|\___| \__,_|_|\__,_|_| \_\|_| .__/| .__/ \___|_|
                                     | |   | |
    """ + Fore.WHITE + r"""   ⚡ Developed by AeroDLL ⚡""" + Fore.RED + r"""    |_|   |_|
    """)
    print(Fore.CYAN + f"{t('supported')}")
    print(Fore.CYAN + "    " + "-"*50 + "\n")

def progress_hook(d):
    if d['status'] == 'downloading':
        p = d.get('_percent_str', '0%').replace('%','')
        s = d.get('_speed_str', 'N/A')
        # İlerleme çubuğu rengini değiştirdim
        print(Fore.CYAN + f"\r    {t('downloading')}: {p}% | {t('speed')}: {s}", end='')
    elif d['status'] == 'finished':
        print(Fore.GREEN + f"\n{t('success')}")

# --- İNDİRME MOTORU ---
def download_content(url, mode):
    
    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'ignoreerrors': True,
    }

    if mode == '1': # VIDEO
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
        print(Fore.MAGENTA + t('video_mode'))
    
    elif mode == '2': # AUDIO
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
        print(Fore.MAGENTA + t('audio_mode'))

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(Fore.YELLOW + t('analyzing'))
            info = ydl.extract_info(url, download=False)
            
            title_vid = info.get('title', t('unknown'))
            print(Fore.WHITE + f"\n {t('target')}: {title_vid}")
            print(Fore.WHITE + f" {t('source')}: {info.get('extractor_key', 'Unknown')}")
            
            ydl.download([url])
            
        print(Fore.GREEN + Style.BRIGHT + f"\n {t('ok_msg')} '{DOWNLOAD_FOLDER}'")
        
        try:
            os.startfile(DOWNLOAD_FOLDER)
        except:
            pass
        
    except Exception as e:
        print(Fore.RED + f"\n {t('error_msg')} {e}")
        print(Fore.YELLOW + t('hint_ffmpeg'))

    print()
    input(Fore.WHITE + t('continue'))

# --- ANA MENÜ ---
def main():
    select_language()
    
    while True:
        banner()
        print(Fore.WHITE + t('menu_1'))
        print(Fore.WHITE + t('menu_2'))
        print(Fore.WHITE + t('menu_3'))
        print(Fore.WHITE + t('menu_4'))
        print(Fore.RED + "\n ══════════════════════════════════════════════════")
        
        choice = input(Fore.RED + t('choice'))
        
        if choice in ['1', '2']:
            url = input(Fore.YELLOW + t('paste_link'))
            if url.strip(): 
                download_content(url, choice)
            
        elif choice == '3':
            url = input(Fore.YELLOW + t('playlist_link'))
            print(Fore.RED + t('playlist_warn'))
            valid_yes = ['e', 'evet'] if LANG == 'TR' else ['y', 'yes']
            
            c = input(t('confirm'))
            if c.lower() in valid_yes: 
                download_content(url, '1')
            
        elif choice == '4':
            sys.exit()

if __name__ == "__main__":
    main()
