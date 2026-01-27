"use client";

import { useEffect, useRef, useState } from "react";
import { MODES, type ModeKey, type Language } from "../lib/modes";
import MessageContent from "../components/MessageContent";

type ChatMessage = { role: "user" | "assistant"; content: string };

type ApiResponse = { reply?: string; error?: string };

export default function HomePage() {
  const [mode, setMode] = useState<ModeKey>("lifehelp");
  const [language, setLanguage] = useState<Language | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");
  const [micSupported, setMicSupported] = useState(false);
  const recognitionRef = useRef<SpeechRecognition | null>(null);

  useEffect(() => {
    const SpeechClass = (window as Window).SpeechRecognition || (window as Window).webkitSpeechRecognition;
    if (!SpeechClass) return;

    setMicSupported(true);
    const rec = new SpeechClass();
    rec.lang = language === "kn" ? "kn-IN" : "en-US";
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
    rec.onerror = () => setStatus(language === "kn" ? "ಮೈಕ್‌ ಉಪಲಬ್ಧವಿಲ್ಲ — ದಯವಿಟ್ಟು ಟೈಪ್ ಮಾಡಿ" : "Mic unavailable — please type instead");
    recognitionRef.current = rec;
  }, [language]);

  const handleLanguageSelect = (lang: Language) => {
    setLanguage(lang);
  };

  const handleSend = async (text?: string) => {
    if (!language) return; // Don't send if no language selected
    const prompt = (text ?? input).trim();
    if (!prompt || loading) return;
    setInput("");
    setLoading(true);
    setStatus(language === "kn" ? "ಆಲೋಚಿಸುತ್ತಿದೆ..." : "Thinking...");
    const userMessage: ChatMessage = { role: "user", content: prompt };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: prompt,
          mode,
          language,
          history: [...messages, userMessage],
        }),
      });
      const data = (await res.json()) as ApiResponse;
      if (!res.ok || data.error) {
        // Handle specific error codes
        let errorMessage = data.error || "Request failed";
        if (res.status === 400) {
          errorMessage = language === "kn" 
            ? "ದಯವಿಟ್ಟು ಮಾನ್ಯವಾದ ಸಂದೇಶವನ್ನು ನಮೂದಿಸಿ" 
            : "Please enter a valid message";
        } else if (res.status === 403) {
          errorMessage = language === "kn" 
            ? "ಅನುಮತಿ ನಿರಾಕರಿಸಲಾಗಿದೆ - ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ" 
            : "Access denied - please try again later";
        } else if (res.status === 429) {
          errorMessage = language === "kn" 
            ? "ತುಂಬಾ ವೇಗವಾಗಿ ವಿನಂತಿಗಳು - ದಯವಿಟ್ಟು ಸ್ವಲ್ಪ ಸಮಯ ಕಾಯಿರಿ" 
            : "Too many requests - please wait a moment";
        }
        throw new Error(errorMessage);
      }
      const reply: ChatMessage = { role: "assistant", content: data.reply || "" };
      setMessages((prev) => [...prev, reply]);
      setStatus("");
    } catch (err) {
      setStatus(err instanceof Error ? err.message : (language === "kn" ? "ಓಹೋ, ಏನೋ ತಪ್ಪಾಗಿದೆ!" : "Uh-oh, something went wrong!"));
    } finally {
      setLoading(false);
    }
  };

  const handleMic = () => {
    if (!micSupported || !recognitionRef.current) {
      setStatus(language === "kn" ? "ಮೈಕ್‌ ಈ ಬ್ರೌಸರ್‌ನಲ್ಲಿ ಬೆಂಬಲಿಸಲ್ಪಟ್ಟಿಲ್ಲ. ದಯವಿಟ್ಟು ಟೈಪ್ ಮಾಡಿ." : "Mic not supported in this browser. Please type instead.");
      return;
    }
    try {
      setStatus(language === "kn" ? "ಕೇಳುತ್ತಿದೆ..." : "Listening...");
      recognitionRef.current.start();
    } catch {
      setStatus(language === "kn" ? "ಮೈಕ್‌ ಕಾರ್ಯನಿರತ. ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ." : "Mic is busy. Try again.");
    }
  };

  const handleDownload = () => {
    if (messages.length === 0) {
      setStatus(language === "kn" ? "ಇನ್ನೂ ಡೌನ್‌ಲೋಡ್ ಮಾಡಲು ಯಾವುದೇ ಸಂಭಾಷಣೆ ಇಲ್ಲ." : "No conversation to download yet.");
      setTimeout(() => setStatus(""), 2000);
      return;
    }

    // Format the conversation
    let content = language === "kn" 
      ? "# ದಕ್ಷಿಣಾಸ್ಯ ದರ್ಶಿನಿಯೊಂದಿಗೆ ಸಂಭಾಷಣೆ\n\n"
      : "# Conversation with Dakshinaasya Darshini\n\n";
    content += `${language === "kn" ? "ದಿನಾಂಕ" : "Date"}: ${new Date().toLocaleDateString()}\n`;
    content += `${language === "kn" ? "ಮೋಡ್" : "Mode"}: ${language === "kn" ? MODES[mode].labelKn : MODES[mode].label}\n\n`;
    content += "---\n\n";

    messages.forEach((msg) => {
      const speaker = msg.role === "user" 
        ? (language === "kn" ? "**ನೀವು**" : "**You**")
        : "**ದರ್ಶಿನಿ**";
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

    setStatus(language === "kn" ? "ಚಾಟ್ ಡೌನ್‌ಲೋಡ್ ಆಗಿದೆ!" : "Chat downloaded!");
    setTimeout(() => setStatus(""), 2000);
  };

  const showHero = messages.length === 0 && language !== null;
  const showLanguageModal = language === null;

  const suggestions = language === "kn" 
    ? [
        "ನಾನು ತುಂಬಾ ದುಃಖದಿಂದಿದ್ದೇನೆ, ನೀವು ನನಗೆ ಸಂತೋಷ ತರಬಹುದೇ?",
        "ನನಗೆ ನನ್ನ ಇಂದ್ರಿಯಗಳನ್ನು ನಿಯಂತ್ರಿಸಲು ಸಾಧ್ಯವಾಗುತ್ತಿಲ್ಲ - ನಾನು ಏನು ಮಾಡಬೇಕು?",
        "ನಾಳೆ ನನಗೆ ಪರೀಕ್ಷೆ ಇದೆ ಮತ್ತು ನಾನು ತುಂಬಾ ಆತಂಕದಿಂದಿದ್ದೇನೆ - ದಯವಿಟ್ಟು ಸಹಾಯ ಮಾಡಿ"
      ]
    : [
        "I'm feeling very sad, can you cheer me up?",
        "I'm not able to control my senses - what can I do?",
        "I have an exam tomorrow & I'm really anxious - help me please"
      ];

  return (
    <main>
      {showLanguageModal && (
        <div className="language-modal-overlay">
          <div className="language-modal">
            <div className="om">ॐ</div>
            <h2>Welcome to Dakshinaasya Darshini</h2>
            <p>Choose your preferred language to begin</p>
            <div className="language-options">
              <div className="language-option" onClick={() => handleLanguageSelect("en")}>
                <div className="lang-emoji">🇬🇧</div>
                <div className="lang-name">English</div>
                <div className="lang-native">English</div>
              </div>
              <div className="language-option" onClick={() => handleLanguageSelect("kn")}>
                <div className="lang-emoji">🇮🇳</div>
                <div className="lang-name">Kannada</div>
                <div className="lang-native">ಕನ್ನಡ</div>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="header-bar" />
      {showHero && (
        <section className="hero">
          <div className="om">ॐ</div>
          <h1>{language === "kn" ? "ನಮಸ್ಕಾರ" : "Namaste"}</h1>
          <p>{language === "kn" 
            ? "ನಾನು ದಕ್ಷಿಣಾಸ್ಯ ದರ್ಶಿನಿ, ನಿಮ್ಮ ಆಧ್ಯಾತ್ಮಿಕ ಮಾರ್ಗದರ್ಶಕ. ನನಗೆ ಏನು ಬೇಕಾದರೂ ಕೇಳಿ."
            : "I am Dakshinaasya Darshini, your spiritual guide. Ask me anything."}
          </p>
          <div className="suggestion-row">
            {suggestions.map((text, idx) => (
              <div key={idx} className="suggestion" onClick={() => handleSend(text)}>
                {text}
              </div>
            ))}
          </div>
        </section>
      )}

      <section className="chat-window">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <h4>{msg.role === "user" ? (language === "kn" ? "ನೀವು" : "You") : (language === "kn" ? "ದರ್ಶಿನಿ" : "Darshini")}</h4>
            <div className="message-content">
              <MessageContent content={msg.content} isAssistant={msg.role === "assistant"} language={language || "en"} />
            </div>
          </div>
        ))}
      </section>

      <div className="input-shell">
        <label className="mode-select">
          <span>{language === "kn" ? "ಮೋಡ್" : "Mode"}</span>
          <select value={mode} onChange={(e) => {
            const newMode = e.target.value as ModeKey;
            if (newMode in MODES) setMode(newMode);
          }}>
            {Object.entries(MODES).map(([key, value]) => (
              <option key={key} value={key}>
                {language === "kn" ? value.labelKn : value.label}
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
          placeholder={language === "kn" ? "ಮೈಕ್ ಟ್ಯಾಪ್ ಮಾಡಿ ಅಥವಾ ಕೆಳಗೆ ಟೈಪ್ ಮಾಡಿ" : "Tap mic to speak or type below"}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
          disabled={!language}
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
        <div className="status-chip">{status || (language === "kn" ? "ಉತ್ಪಾದಿಸುತ್ತಿದೆ..." : "Generating...")}</div>
      )}
    </main>
  );
}
