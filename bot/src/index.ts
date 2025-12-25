import {
  Client,
  Events,
  GatewayIntentBits,
} from "discord.js";
import "dotenv/config";
import { config } from "./config.js";

const client = new Client({
  intents: [GatewayIntentBits.Guilds],
});

client.once(Events.ClientReady, (readyClient) => {
  console.log(`Bot is online as ${readyClient.user.tag}`);
});

client.on(Events.InteractionCreate, async (interaction) => {
  if (!interaction.isChatInputCommand()) {
    return;
  }

  if (interaction.commandName === "ping") {
    await interaction.reply("Pong!");
  }

  if (interaction.commandName === "status") {
    await interaction.deferReply();

    try {
      const response = await fetch(`${config.BACKEND_URL}/health`);
      const data = await response.json();

      await interaction.editReply(
        `**Backend Status**\n` +
        `Status: ${data.status}\n` +
        `Uptime: ${data.uptime_seconds}s\n` +
        `Version: ${data.version}`
      );
    } catch (error) {
      await interaction.editReply("Backend is offline or unreachable.");
    }
  }
});


client.login(config.DISCORD_TOKEN);
