from discord_winhook.screenshot import SSHook

import pygetwindow as gw
hook = SSHook(
    "{webhook}",
    gw.getActiveWindow(),
)

hook.recur(5*60)
