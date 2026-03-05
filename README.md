# PyMyMC

A lightweight Minecraft launcher built with Python and PyQt5.

<img width="1530" height="1087" alt="image" src="https://github.com/user-attachments/assets/a91f009f-2a77-4bef-8204-12ddbd6e2074" />



## Features

- **Version Manager** — Browse, search, download, and delete Minecraft versions from a dedicated dialogue. Filter by releases or view all snapshots and betas.
- **All versions supported** — Every version available through the official launcher, including snapshots, betas, and historical releases.
- **Custom JVM configuration** — Set RAM allocation, JVM arguments, and point to a custom Java executable.
- **Quick Connect** — Auto-connect to a server on launch.
- **Custom resolution** — Launch with a specific window size.
- **Non-premium support** — Works with both premium and offline accounts.

## Installation

Download the latest binary from [GitHub Releases](https://github.com/RealistikDash/PyMyMC/releases).

## Development

```bash
make install   # Install dependencies
make run       # Run the launcher
make lint      # Lint/format (ruff via pre-commit)
make build     # Build binary (Nuitka)
make clean     # Remove build artifacts
```

## Configuration

Settings are stored in `config.json` (created on first run). Everything can be configured through the in-app Settings dialogue.
