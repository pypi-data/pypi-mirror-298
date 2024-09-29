import psutil
import platform
from datetime import datetime

from discord_winhook.base import Hook

class MachineStatusHook(Hook):
    def run(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        
        status = {
            "os": platform.system(),
            "os version": platform.version(),
            "cpu usage": f"{cpu_usage}%",
            "memory total": f"{memory.total / (1024 ** 3):.2f} GB",
            "memory used": f"{memory.used / (1024 ** 3):.2f} GB",
            "memory percent": f"{memory.percent}%",
            "disk total": f"{disk.total / (1024 ** 3):.2f} GB",
            "disk used": f"{disk.used / (1024 ** 3):.2f} GB",
            "disk percent": f"{disk.percent}%",
            "boot time": boot_time
        }
        
        from discord_webhook import DiscordWebhook, DiscordEmbed

        webhook = DiscordWebhook(url=self.url)

        embed = DiscordEmbed(title="Machine Status", color="03b2f8")

        for key, value in status.items():
            embed.add_embed_field(name=key.title(), value=value, inline=True)

        webhook.add_embed(embed)
        self._Hook__send(webhook)

    
