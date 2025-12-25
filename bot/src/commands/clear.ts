/** Clear command - reset conversation history. */

import { ChatInputCommandInteraction } from "discord.js";
import { config } from "../config";

export async function execute(interaction: ChatInputCommandInteraction) {
  await interaction.deferReply();

  try {
    await fetch(
      `${config.BACKEND_URL}/chat/clear?user_id=${interaction.user.id}`,
      {
        method: "POST",
      }
    );
    await interaction.editReply("Conversation history cleared!");
  } catch (_error) {
    await interaction.editReply("Failed to clear history.");
  }
}
