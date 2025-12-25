import "dotenv/config";
import {
  REST,
  Routes,
  SlashCommandBuilder
} from "discord.js";

const token = process.env.DISCORD_TOKEN!;
const clientId = process.env.DISCORD_CLIENT_ID!;

const commands = [
  new SlashCommandBuilder()
    .setName("ping")
    .setDescription("Replies with Pong!")
].map((command) => command.toJSON());

const rest = new REST().setToken(token);

console.log("Registering slash commands...");

rest
  .put(
    Routes.applicationCommands(clientId),
    {
      body: commands
    })
  .then(() => console.log("Successfully registered commands!"))
  .catch(console.error);
