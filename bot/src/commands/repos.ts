/**
 * /repos command - Manage watched GitHub repos for this server
 * Subcommands: list, add, remove
 */

import { ChatInputCommandInteraction } from "discord.js";
import { config } from "../config";

export async function execute(
  interaction: ChatInputCommandInteraction
): Promise<void> {
  const subcommand = interaction.options.getSubcommand();
  const guildId = interaction.guildId;

  if (!guildId) {
    await interaction.reply("This command can only be used in a server.");
    return;
  }

  await interaction.deferReply();

  try {
    if (subcommand === "list") {
      await handleList(interaction, guildId);
    } else if (subcommand === "add") {
      await handleAdd(interaction, guildId);
    } else if (subcommand === "remove") {
      await handleRemove(interaction, guildId);
    }
  } catch (error) {
    console.error("Repos command error:", error);
    await interaction.editReply("Failed to manage repos. Is the backend running?");
  }
}
