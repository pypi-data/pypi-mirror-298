# discord-winhook
A library to simplify sending information updates from Windows systems through a Discord webhook

## Install
```bash
pip install discord-winhook
```

## Usage
```py
from discord_winhook import SSHook
import pygetwindow as gw
hook = SSHook(
    "{webhook_url}",
    gw.getActiveWindow(),
)
# send every 5 minutes
hook.recur(5*60)
```

