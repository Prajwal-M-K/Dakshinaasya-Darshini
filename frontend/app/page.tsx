"use client";

import { useEffect, useRef, useState } from "react";
import { MODES, type ModeKey } from "../lib/modes";
import MessageContent from "../components/MessageContent";

type ChatMessage = { role: "user" | "assistant"; content: string };

type ApiResponse = { reply?: string; error?: string };

type SpeechConstructor = new () => SpeechRecognition;


export default function HomePage() {
  const [mode, setMode] = useState<ModeKey>("lifehelp");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");
  const [micSupported, setMicSupported] = useState(false);
  const recognitionRef = useRef<SpeechRecognition | null>(null);

  useEffect(() => {
    const SpeechClass: SpeechConstructor | undefined =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechClass) return;

    setMicSupported(true);
    const rec = new SpeechClass();
    rec.lang = "en-US";
    rec.continuous = false;
    rec.interimResults = false;
    rec.maxAlternatives = 1;
    rec.onresult = (event: SpeechRecognitionEvent) => {
      const transcript = event.results?.[0]?.[0]?.transcript;
      if (transcript) {
        setInput((prev) => (prev ? `${prev} ${transcript}` : transcript));
      }
    };
    rec.onend = () => setStatus("");
    rec.onerror = () => setStatus("Mic unavailable — please type instead");
    recognitionRef.current = rec;
  }, []);

  const handleSend = async (text?: string) => {
    const prompt = (text ?? input).trim();
    if (!prompt || loading) return;
    setInput("");
    setLoading(true);
    setStatus("Thinking...");
    const userMessage: ChatMessage = { role: "user", content: prompt };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: prompt,
          mode,
          history: [...messages, userMessage],
        }),
      });
      const data = (await res.json()) as ApiResponse;
      if (!res.ok || data.error) {
        throw new Error(data.error || "Request failed");
      }
      const reply: ChatMessage = { role: "assistant", content: data.reply || "" };
      setMessages((prev) => [...prev, reply]);
      setStatus("");
    } catch (err) {
      setStatus(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const handleMic = () => {
    if (!micSupported || !recognitionRef.current) {
      setStatus("Mic not supported in this browser. Please type instead.");
      return;
    }
    try {
      setStatus("Listening...");
      recognitionRef.current.start();
    } catch {
      setStatus("Mic is busy. Try again.");
    }
  };

  const showHero = messages.length === 0;

  return (
    <main>
      <div className="header-bar" />
      {showHero && (
        <section className="hero">
          <div className="om">ॐ</div>
          <h1>Namaste</h1>
          <p>I am Dakshinaasya Darshini, your spiritual guide. Ask me anything.</p>
        </section>
      )}

      <section className="chat-window">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <h4>{msg.role === "user" ? "You" : "Darshini"}</h4>
            <div className="message-content">
              <MessageContent content={msg.content} />
            </div>
          </div>
        ))}
      </section>

      <div className="input-shell">
        <label className="mode-select">
          <span>Mode</span>
          <select value={mode} onChange={(e) => {
            const newMode = e.target.value as ModeKey;
            if (newMode in MODES) setMode(newMode);
          }}>
            {Object.entries(MODES).map(([key, value]) => (
              <option key={key} value={key}>
                {value.label}
              </option>
            ))}
          </select>
        </label>

        <input
          className="text-entry"
          placeholder="Tap mic to speak or type below"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
        />

        <div className="actions">
          <button className="action-btn" title="Voice input" onClick={handleMic}>
            🎙️
          </button>
          <button
            className="action-btn primary"
            title="Send"
            onClick={() => handleSend()}
            disabled={loading}
          >
            ➤
          </button>
        </div>
      </div>
      <div className="status-chip">{status || (loading ? "Generating..." : "")}</div>
    </main>
  );
}
