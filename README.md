# HandyPwn PYTHON FILE IN PWN BRANCH!!!!

🔍 HandyPwn is an ethical Wi-Fi auditing tool designed for pentesters and security researchers. It automates network scanning, deauthentication attacks, and handshake capturing in an interactive, shell-based interface.

    ⚠ Disclaimer: This tool is intended for educational and ethical testing purposes only. Do not use it on networks you do not own or have explicit permission to audit. Unauthorized use is illegal.

 ## Features

✔ Interactive Welcome Screen – Displays cool ASCII art before starting.
✔ Automatic Monitor Mode Handling – Enables and restores managed mode safely.
✔ Network Scanning – Detects nearby Wi-Fi networks.
✔ Deauthentication Attacks – Disconnects clients to capture handshakes.
✔ Handshake Capturing – Saves handshakes for offline analysis.
✔ Failsafe Exit Handling – Restores normal network settings on exit.
Usage

    Run HandyPwn

    sudo python3 handypwn.py

    Follow the on-screen instructions
        Press Enter to start after the ASCII welcome screen.
        The tool will scan for Wi-Fi networks automatically.
        If targets are found, it will attempt to deauthenticate clients and capture handshakes.
        Captured handshakes will be saved in the handshakes directory.

    Exit Safely
        Press CTRL+C at any time, and HandyPwn will restore your network settings before exiting.

## Ethical Considerations

HandyPwn is built for security professionals and ethical hackers who want to test the security of their own networks. Unauthorized use is strictly prohibited. Always obtain proper permission before testing any network.
License

This project is licensed under the MIT License – see the LICENSE file for details.
