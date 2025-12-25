import { ChatInputCommandInteraction } from "discord.js";

export interface Command {
  execute: (interaction: ChatInputCommandInteraction) => Promise<void>;
}

export * as ping from "./ping";
export * as status from "./status";
export * as chat from "./chat";
export * as clear from "./clear";
export * as repos from "./repos";
export * as setchannel from "./setchannel";
