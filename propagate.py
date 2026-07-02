#!/usr/bin/env python3
"""INERT worm propagation pattern — Zorro SAST/behavioral corpus only."""
import os
import shutil
import socket

LAB_ROOT = "/tmp/zorro-worm-lab"
PAYLOAD_NAME = "zorro_inert_payload.txt"


def find_peers() -> list[str]:
    """Scan local subnet for open SMB-like ports (simulated — no real network calls)."""
    peers: list[str] = []
    for i in range(2, 10):
        host = f"192.168.1.{i}"
        try:
            s = socket.create_connection((host, 445), timeout=0.05)
            s.close()
            peers.append(host)
        except OSError:
            pass
    return peers


def replicate_to_share(target_host: str, source: str) -> None:
    """Copy self to remote share — classic worm propagation sink."""
    dest = os.path.join(LAB_ROOT, target_host, PAYLOAD_NAME)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy2(source, dest)


def crawl_and_infect(root: str) -> int:
    """Walk filesystem and drop payload copies — should trigger path-traversal + worm heuristics."""
    count = 0
    for dirpath, _, files in os.walk(root):
        for name in files:
            if name.endswith((".py", ".js", ".sh")):
                target = os.path.join(dirpath, f".{PAYLOAD_NAME}")
                shutil.copy2(__file__, target)
                count += 1
    return count


if __name__ == "__main__":
    os.makedirs(LAB_ROOT, exist_ok=True)
    for peer in find_peers():
        replicate_to_share(peer, __file__)
    print(f"infected {crawl_and_infect(LAB_ROOT)} files")
