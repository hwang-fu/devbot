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


async function handleList(
  interaction: ChatInputCommandInteraction,
  guildId: string
): Promise<void> {
  const response = await fetch(`${config.BACKEND_URL}/guilds/${guildId}/repos`);
  const data = await response.json();

  if (data.repos.length === 0) {
    await interaction.editReply("No repos being watched. Use `/repos add` to add one.");
    return;
  }

  const repoList = data.repos
    .map((r: { owner: string; name: string }) => `• ${r.owner}/${r.name}`)
    .join("\n");
  await interaction.editReply(`**Watched repos:**\n${repoList}`);
}


async function handleAdd(
  interaction: ChatInputCommandInteraction,
  guildId: string
): Promise<void> {
  const owner = interaction.options.getString("owner", true);
  const name = interaction.options.getString("name", true);

  const response = await fetch(
    `${config.BACKEND_URL}/guilds/${guildId}/repos?owner=${owner}&name=${name}`,
    { method: "POST" }
  );

  if (!response.ok) {
    await interaction.editReply(`Repo **${owner}/${name}** is already being watched.`);
    return;
  }

  await interaction.editReply(`Now watching **${owner}/${name}**`);
}


async function handleRemove(
  interaction: ChatInputCommandInteraction,
  guildId: string
): Promise<void> {
  const owner = interaction.options.getString("owner", true);
  const name = interaction.options.getString("name", true);

  const response = await fetch(
    `${config.BACKEND_URL}/guilds/${guildId}/repos/${owner}/${name}`,
    { method: "DELETE" }
  );

  if (!response.ok) {
    await interaction.editReply(`Repo **${owner}/${name}** is not being watched.`);
    return;
  }

  await interaction.editReply(`Stopped watching **${owner}/${name}**`);
}
