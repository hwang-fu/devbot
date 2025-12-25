/**
  * /setchannel command - Set the channel for GitHub notifications
  */

import { ChatInputCommandInteraction, ChannelType } from "discord.js";
import { config } from "../config";

export async function execute(
  interaction: ChatInputCommandInteraction
): Promise<void> {
  const guildId = interaction.guildId;

  if (!guildId) {
    await interaction.reply("This command can only be used in a server.");
    return;
  }

  const channel = interaction.options.getChannel("channel", true);

  // Verify it's a text channel
  if (channel.type !== ChannelType.GuildText) {
    await interaction.reply("Please select a text channel.");
    return;
  }

  await interaction.deferReply();

  try {
    const response = await fetch(
      `${config.BACKEND_URL}/guilds/${guildId}/config?notification_channel_id=${channel.id}`,
      { method: "PUT" }
    );

    if (!response.ok) {
      await interaction.editReply("Failed to set notification channel.");
      return;
    }

    await interaction.editReply(
      `GitHub notifications will be sent to <#${channel.id}>`
    );
  } catch (error) {
    console.error("Setchannel error:", error);
    await interaction.editReply("Failed to set channel. Is the backend running?");
  }
}
