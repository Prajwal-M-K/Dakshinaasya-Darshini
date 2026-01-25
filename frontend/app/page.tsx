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

  const handleDownload = () => {
    if (messages.length === 0) {
      setStatus("No conversation to download yet.");
      setTimeout(() => setStatus(""), 2000);
      return;
    }

    // Format the conversation
    let content = "# Conversation with Dakshinaasya Darshini\n\n";
    content += `Date: ${new Date().toLocaleDateString()}\n`;
    content += `Mode: ${MODES[mode].label}\n\n`;
    content += "---\n\n";

    messages.forEach((msg) => {
      const speaker = msg.role === "user" ? "**You**" : "**Darshini**";
      content += `${speaker}:\n${msg.content}\n\n`;
    });

    // Create blob and download
    const blob = new Blob([content], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `darshini-chat-${Date.now()}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    setStatus("Chat downloaded!");
    setTimeout(() => setStatus(""), 2000);
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
          <div className="suggestion-row">
            <div className="suggestion" onClick={() => handleSend("I'm feeling very sad, can you cheer me up?")}>
              I&apos;m feeling very sad, can you cheer me up?
            </div>
            <div className="suggestion" onClick={() => handleSend("I'm not able to control my senses - what can I do?")}>
              I&apos;m not able to control my senses - what can I do?
            </div>
            <div className="suggestion" onClick={() => handleSend("I have an exam tomorrow & I'm really anxious - help me please")}>
              I have an exam tomorrow &amp; I&apos;m really anxious - help me please
            </div>
          </div>
        </section>
      )}

      <section className="chat-window">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <h4>{msg.role === "user" ? "You" : "Darshini"}</h4>
            <div className="message-content">
              <MessageContent content={msg.content} isAssistant={msg.role === "assistant"} />
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

        {messages.length > 0 && (
          <button 
            className="download-btn" 
            onClick={handleDownload}
            title="Download conversation"
          >
            💾
          </button>
        )}

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
      {(status || loading) && (
        <div className="status-chip">{status || "Generating..."}</div>
      )}
    </main>
  );
}
