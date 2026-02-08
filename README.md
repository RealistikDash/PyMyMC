# PyMyMC

A lightweight Minecraft launcher built with Python and PyQt5.

<img width="853" height="567" alt="image" src="https://github.com/user-attachments/assets/83dfc511-6700-4f3d-bb98-86e0eda856fd" />

## Features

- **Version Manager** — Browse, search, download, and delete Minecraft versions from a dedicated dialogue. Filter by releases or view all snapshots and betas.
- **All versions supported** — Every version available through the official launcher, including snapshots, betas, and historical releases.
- **Custom JVM configuration** — Set RAM allocation, JVM arguments, and point to a custom Java executable.
- **Quick Connect** — Auto-connect to a server on launch.
- **Custom resolution** — Launch with a specific window size.
- **Non-premium support** — Works with both premium and offline accounts.
- **Discord Rich Presence** — Optional integration via pypresence.

## Installation

Requires Python 3.7+.

```bash
pip install -r requirements.txt
python -m pymymc
```

## Configuration

Settings are stored in `config.json` (created on first run). Everything can be configured through the in-app Settings dialogue.
