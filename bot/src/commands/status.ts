/** Status command - check backend health. */

import { ChatInputCommandInteraction } from "discord.js";
import { config } from "../config";

export async function execute(interaction: ChatInputCommandInteraction) {
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
