import { NextResponse } from "next/server";
import { GoogleGenerativeAI } from "@google/generative-ai";
import fs from "fs";
import path from "path";
import { MODES, buildSystemPrompt, ModeKey } from "../../../lib/modes";

type ChatMessage = { role: "user" | "assistant"; content: string };

type Payload = {
  message: string;
  mode?: ModeKey;
  history?: ChatMessage[];
};

let cachedContext: string | null = null;

function loadContext(): string {
  if (cachedContext) return cachedContext;
  const contextPath = path.join(process.cwd(), "Dakshina_Murthi_Context.txt");
  if (!fs.existsSync(contextPath)) {
    throw new Error("Context file not found");
  }
  cachedContext = fs.readFileSync(contextPath, "utf8");
  return cachedContext;
}

export async function POST(req: Request) {
  try {
    const body = (await req.json()) as Payload;
    const message = body.message?.trim();
    const mode: ModeKey = body.mode ?? "lifehelp";
    const history = body.history ?? [];

    if (!message) {
      return NextResponse.json({ error: "Message is required" }, { status: 400 });
    }
    if (!MODES[mode]) {
      return NextResponse.json({ error: "Invalid mode" }, { status: 400 });
    }

    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
      return NextResponse.json({ error: "GEMINI_API_KEY missing" }, { status: 500 });
    }

    const context = loadContext();
    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({
      model: "gemini-2.5-flash",
      systemInstruction: buildSystemPrompt(mode, context),
      generationConfig: {
        temperature: 0.7,
        maxOutputTokens: MODES[mode].maxTokens,
      },
    });

    const chat = model.startChat({
      history: history.map((m) => ({
        role: m.role === "user" ? "user" : "model",
        parts: [{ text: m.content }],
      })),
    });

    const result = await chat.sendMessage(message);
    const reply = result.response.text();

    return NextResponse.json({ reply });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
