"use client";

import ReactMarkdown from "react-markdown";

export default function MessageContent({ content }: { content: string }) {
  return <ReactMarkdown>{content}</ReactMarkdown>;
}
