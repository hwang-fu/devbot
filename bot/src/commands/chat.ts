/** Chat command - AI conversation with memory. */

import { ChatInputCommandInteraction } from "discord.js";
import { config } from "../config";

export async function execute(interaction: ChatInputCommandInteraction) {
  const message = interaction.options.getString("message", true);
  await interaction.deferReply();

  try {
    const response = await fetch(`${config.BACKEND_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: interaction.user.id,
        message: message,
      }),
    });
    const data = await response.json();
    await interaction.editReply(data.response);
  } catch (_error) {
    await interaction.editReply("Failed to get AI response.");
  }
}
