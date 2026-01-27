"use client";

import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import type { Language } from "../lib/modes";

export default function MessageContent({ 
  content, 
  isAssistant = false,
  language = "en"
}: { 
  content: string;
  isAssistant?: boolean;
  language?: Language;
}) {
  const [speaking, setSpeaking] = useState(false);
  const [kannadaVoiceAvailable, setKannadaVoiceAvailable] = useState(false);

  useEffect(() => {
    // Check if Kannada voice is available in speech synthesis
    if ('speechSynthesis' in window) {
      const checkVoices = () => {
        const voices = window.speechSynthesis.getVoices();
        const hasKannada = voices.some(v => 
          v.lang.startsWith('kn') || v.lang.includes('kn-IN')
        );
        setKannadaVoiceAvailable(hasKannada);
      };
      
      // Check immediately and on voice change
      checkVoices();
      window.speechSynthesis.onvoiceschanged = checkVoices;
    }
  }, []);

  const handleSpeak = () => {
    // Stop any ongoing speech
    if (speaking) {
      window.speechSynthesis?.cancel();
      setSpeaking(false);
      return;
    }

    // Create text to speak (strip markdown formatting)
    const textToSpeak = content
      .replace(/!\[[^\]]*\]\([^)]*\)/g, '')   // Remove images
      .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // Keep link text, remove url
      .replace(/[#*_`]/g, '')                  // Remove decoration chars
      .trim();
    
    // Only proceed if native voice is available
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(textToSpeak);
      
      if (language === "kn") {
        utterance.lang = "kn-IN";
        utterance.rate = 0.8;
      } else {
        utterance.lang = "en-US";
        utterance.rate = 0.9;
      }
      
      utterance.onstart = () => setSpeaking(true);
      utterance.onend = () => setSpeaking(false);
      utterance.onerror = () => setSpeaking(false);
      
      window.speechSynthesis.speak(utterance);
    }
  };

  const speakButtonIcon = speaking ? '⏸️' : '🔊';

  const speakButtonTitle = language === "kn"
    ? (speaking ? "ನಿಲ್ಲಿಸಿ" : "ಕೇಳಿ")
    : (speaking ? "Stop" : "Listen");

  // Only show button if English or if Kannada voice is explicitly available
  const showButton = isAssistant && (language === "en" || (language === "kn" && kannadaVoiceAvailable));

  return (
    <div className="message-content-wrapper">
      {showButton && (
        <button
          className="speak-btn-small"
          onClick={handleSpeak}
          title={speakButtonTitle}
        >
          {speakButtonIcon} {language === "kn" ? (speaking ? "ನಿಲ್ಲಿಸಿ" : "ಕೇಳಿ") : (speaking ? "Stop" : "Listen")}
        </button>
      )}
      <ReactMarkdown>{content}</ReactMarkdown>
    </div>
  );
}
