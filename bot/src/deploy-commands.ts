/**
 * Slash command registration script.
 * Run this once (or when commands change) to register with Discord API.
 * Usage: npx tsx src/deploy-commands.ts
 */
import "dotenv/config";
import {
  REST,
  Routes,
  ChannelType,
  SlashCommandBuilder,
} from "discord.js";

const token = process.env.DISCORD_TOKEN!;
const clientId = process.env.DISCORD_CLIENT_ID!;

const commands = [
  new SlashCommandBuilder()
    .setName("ping")
    .setDescription("Replies with Pong!"),


  new SlashCommandBuilder()
    .setName("status")
    .setDescription("Check bot and backend health"),


  new SlashCommandBuilder()
    .setName("chat")
    .setDescription("Chat with AI")
    .addStringOption((option) =>
      option
        .setName("message")
        .setDescription("Your message")
        .setRequired(true)
    ),


  new SlashCommandBuilder()
    .setName("clear")
    .setDescription("Clear your conversation history"),


  new SlashCommandBuilder()
    .setName("repos")
    .setDescription("Manage watched GitHub repos")
    .addSubcommand((sub) =>
      sub
        .setName("list")
        .setDescription("List watched repos")
    )
    .addSubcommand((sub) =>
      sub
        .setName("add")
        .setDescription("Add a repo to watch")
        .addStringOption((opt) =>
          opt
            .setName("owner")
            .setDescription("Repo owner")
            .setRequired(true)
        )
        .addStringOption((opt) =>
          opt
            .setName("name")
            .setDescription("Repo name")
            .setRequired(true)
        )
    )
    .addSubcommand((sub) =>
      sub
        .setName("remove")
        .setDescription("Remove a watched repo")
        .addStringOption((opt) =>
          opt
            .setName("owner")
            .setDescription("Repo owner")
            .setRequired(true)
        )
        .addStringOption((opt) =>
          opt
            .setName("name")
            .setDescription("Repo name")
            .setRequired(true)
        )
    ),

  new SlashCommandBuilder()
    .setName("setchannel")
    .setDescription("Set channel for GitHub notifications")
    .addChannelOption((opt) =>
      opt
        .setName("channel")
        .setDescription("The channel to send notifications to")
        .setRequired(true)
    ),
].map((command) => command.toJSON());

const rest = new REST().setToken(token);

console.log("Registering slash commands...");

rest
  .put(Routes.applicationCommands(clientId), {
    body: commands,
  })
  .then(() => console.log("Successfully registered commands!"))
  .catch(console.error);
