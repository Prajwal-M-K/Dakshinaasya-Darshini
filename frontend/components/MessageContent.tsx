"use client";

import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";

export default function MessageContent({ 
  content, 
  isAssistant = false 
}: { 
  content: string;
  isAssistant?: boolean;
}) {
  const [speaking, setSpeaking] = useState(false);
  const [speechSupported, setSpeechSupported] = useState(false);

  useEffect(() => {
    // Check if speech synthesis is supported
    setSpeechSupported('speechSynthesis' in window);
  }, []);

  const handleSpeak = () => {
    if (!speechSupported || !window.speechSynthesis) return;

    // Stop any ongoing speech
    if (speaking) {
      window.speechSynthesis.cancel();
      setSpeaking(false);
      return;
    }

    // Create utterance from content (strip markdown formatting)
    const textToSpeak = content.replace(/[#*_`[\]()]/g, '');
    const utterance = new SpeechSynthesisUtterance(textToSpeak);
    utterance.rate = 0.9; // Slightly slower for clarity

    utterance.onstart = () => setSpeaking(true);
    utterance.onend = () => setSpeaking(false);
    utterance.onerror = () => setSpeaking(false);

    window.speechSynthesis.speak(utterance);
  };

  return (
    <div className="message-content-wrapper">
      <ReactMarkdown>{content}</ReactMarkdown>
      {isAssistant && speechSupported && (
        <button
          className="speak-btn"
          onClick={handleSpeak}
          title={speaking ? "Stop speaking" : "Read aloud"}
        >
          {speaking ? '⏸️ Stop' : '🔊 Listen'}
        </button>
      )}
    </div>
  );
}
