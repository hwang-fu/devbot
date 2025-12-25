/**
 * Configuration module with Zod validation.
 * Validates environment variables at startup (fail-fast pattern).
 */
import { z } from "zod";

const envSchema = z.object({
  DISCORD_TOKEN: z.string().min(1, "DISCORD_TOKEN is required"),
  DISCORD_CLIENT_ID: z.string().min(1, "DISCORD_CLIENT_ID is required"),
  BACKEND_URL: z.string().url("BACKEND_URL must be a valid URL"),
});

/** Load and validate configuration from environment variables. */
function loadConfig() {
  const result = envSchema.safeParse(process.env);
  if (!result.success) {
    console.error("Invalid configuration:");
    result.error.issues.forEach((issue) => {
      console.error(`  - ${issue.path.join(".")}: ${issue.message}`);
    });
    process.exit(1);
  }
  return result.data
}

export const config = loadConfig();
