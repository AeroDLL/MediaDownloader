import os
import sys
import time
from colorama import init, Fore, Style
import yt_dlp

# Renkleri Başlat
init(autoreset=True)

# --- AYARLAR ---
DOWNLOAD_FOLDER = "Downloads"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# --- YARDIMCI FONKSIYONLAR ---
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def title(text):
    os.system(f'title MediaRipper v1.0 | {text}')

def banner():
    clear()
    print(Fore.MAGENTA + Style.BRIGHT + r"""
    ╔══════════════════════════════════════════════════════════╗
    ║  ███╗   ███╗███████╗██████╗ ██╗ █████╗ ██████╗           ║
    ║  ████╗ ████║██╔════╝██╔══██╗██║██╔══██╗██╔══██╗          ║
    ║  ██╔████╔██║█████╗  ██║  ██║██║███████║██████╔╝          ║
    ║  ██║╚██╔╝██║██╔══╝  ██║  ██║██║██╔══██║██╔══██╗          ║
    ║  ██║ ╚═╝ ██║███████╗██████╔╝██║██║  ██║██║  ██║ v1.0     ║
    ║  ╚═╝     ╚═╝╚══════╝╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝          ║
    ║        ULTIMATE MULTI-PLATFORM DOWNLOADER                ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    print(Fore.CYAN + "    Supported: YouTube, Instagram, TikTok, X, Twitch\n")

def progress_hook(d):
    if d['status'] == 'downloading':
        p = d.get('_percent_str', '0%').replace('%','')
        print(Fore.YELLOW + f"\r    [download] İndiriliyor: {p}% | Hız: {d.get('_speed_str', 'N/A')}", end='')
    elif d['status'] == 'finished':
        print(Fore.GREEN + "\n    [success] İndirme tamamlandı! Dönüştürülüyor...")

# --- İNDİRME MOTORU ---
def download_content(url, mode):
    # mode 1: Video (Best Quality)
    # mode 2: Audio Only (MP3)
    
    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
    }

    if mode == '1': # Video
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
        print(Fore.CYAN + " [*] En iyi video kalitesi ayarlandi...")
    
    elif mode == '2': # Audio (MP3)
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
        print(Fore.CYAN + " [*] MP3 Dönüştürücü ayarlandi (FFmpeg)...")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            print(Fore.WHITE + f"\n [Target]: {info.get('title', 'Unknown')}")
            print(Fore.WHITE + f" [Source]: {info.get('extractor_key', 'Unknown')}")
            
            ydl.download([url])
            
        print(Fore.GREEN + f"\n [OK] İşlem Başarılı! Dosya '{DOWNLOAD_FOLDER}' klasöründe.")
        
    except Exception as e:
        print(Fore.RED + f"\n [ERROR] Hata oluştu: {e}")
        print(Fore.YELLOW + " İpucu: FFmpeg yüklü mü? Link doğru mu?")

    input(Fore.WHITE + "\n Devam etmek için Enter...")

# --- ANA MENÜ ---
def main():
    while True:
        banner()
        print(Fore.WHITE + "  [1] 🎬 Video İndir (Max Kalite / 4K)")
        print(Fore.WHITE + "  [2] 🎵 Müzik İndir (MP3 Dönüştür)")
        print(Fore.WHITE + "  [3] 📋 Oynatma Listesi (Playlist) İndir")
        print(Fore.WHITE + "  [4] ❌ Çıkış")
        print(Fore.CYAN + "\n ==========================================================")
        
        choice = input(Fore.GREEN + "  Seçiminiz (1-4): ")
        
        if choice in ['1', '2']:
            url = input(Fore.YELLOW + "  Link'i Yapıştır (URL): ")
            if url: download_content(url, choice)
            
        elif choice == '3':
            url = input(Fore.YELLOW + "  Playlist Linki: ")
            print(Fore.RED + "  [!] Uyarı: Playlist indirmek uzun sürebilir.")
            c = input("  Onaylıyor musun? (e/h): ")
            if c.lower() == 'e': download_content(url, '1') # Playlist video olarak iner
            
        elif choice == '4':
            sys.exit()

if __name__ == "__main__":
    main()
