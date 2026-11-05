---
name: enable-wake-on-lan-and-auto-shutdown-on-network-loss-for-ras
description: "Enable Wake-on-LAN and auto-shutdown on network loss for Raspberry Pi."
version: 1.0.0
author: DracieVajko
tags: [raspberry-pi, wake-on-lan, auto-shutdown, network-monitoring, systemd]
category: engineering-3d
source_repository: https://github.com/DracieVajko/Dracievajko-SkillsSet
source_file: skills/original/enable-wake-on-lan-and-auto-shutdown-on-network-loss-for-ras/SKILL.md
license: MIT
local_modifications: original
verification_status: verified
authorship: original
---

# Enable Wake-on-LAN and Auto-Shutdown on Network Loss for Raspberry Pi

Configure a Raspberry Pi to wake from sleep via Wake-on-LAN and automatically shut down when network connectivity is lost.

## When to Use

- Configuring a Raspberry Pi to wake from sleep via Wake-on-LAN and automatically shut down when network connectivity is lost.
- Not for general Linux system administration or other networking tasks.

## Procedure

1. Install required packages: `sudo apt-get update && sudo apt-get install -y ethtool wakeonlan`.
2. Enable Wake-on-LAN on the Ethernet interface: `sudo ethtool -s eth0 wol g`.
3. Create a systemd unit (e.g., `/etc/systemd/system/wol-keepalive.service`) that runs a script on boot to re-enable WoL after each reboot.
4. Write a monitoring script (e.g., `/usr/local/bin/net-watch.sh`) that pings a reliable host (e.g., 8.8.8.8) in a loop and calls `sudo shutdown -h now` after a configurable timeout of failed pings.
5. Create a systemd service (e.g., `/etc/systemd/system/net-watch.service`) that starts the monitoring script at boot.
6. Enable and start both services: `sudo systemctl enable --now wol-keepalive.service net-watch.service`.

## Pitfalls

- Forgetting to re-enable WoL after reboot.
- Using an unreliable ping target.
- Insufficient timeout before shutdown.

## Verification

- `ethtool` shows WoL enabled (`g`).
- Both systemd services are active and enabled.
- Network loss triggers shutdown within the configured timeout.
