import React from "react";
import ChatWindow from "./components/ChatWindow";
import { BACKEND_URL } from "./config";

export default function App() {
  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-3">📱 Phone Recommender Chatbot</h1>
      <ChatWindow backendUrl={BACKEND_URL} />
    </div>
  );
}
