/**
 * Discord bot entry point.
 * Handles client connection and routes commands to handlers.
 */

import { Client, Events, GatewayIntentBits } from "discord.js";
import "dotenv/config";
import { config } from "./config";
import { Command, ping, status, chat, clear } from "./commands";

const client = new Client({
  intents: [GatewayIntentBits.Guilds],
});

client.once(Events.ClientReady, (readyClient) => {
  console.log(`Bot is online as ${readyClient.user.tag}`);
});

client.on(Events.InteractionCreate, async (interaction) => {
  if (!interaction.isChatInputCommand()) return;

  const commands: Record<string, Command> = {
    ping,
    status,
    chat,
    clear,
  };

  const command = commands[interaction.commandName];
  if (command) {
    await command.execute(interaction);
  }
});

client.login(config.DISCORD_TOKEN);
