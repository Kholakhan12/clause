
"use client";

import { useState } from "react";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function askQuestion() {
    if (!question.trim()) return;

    setLoading(true);
    setAnswer("");
    setError("");

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      const data = await response.json();

      setAnswer(
        data.answer ??
        data.response ??
        data.result ??
        JSON.stringify(data, null, 2)
      );
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-gray-950 text-white flex">
      {/* Sidebar */}
      <aside className="w-64 bg-gray-900 border-r border-gray-800 p-6 hidden md:block">
        <h1 className="text-2xl font-bold text-blue-400">
          Clause AI
        </h1>

        <p className="text-gray-400 text-sm mt-2">
          Intelligent Document Assistant
        </p>

        <button
          onClick={() => {
            setQuestion("");
            setAnswer("");
            setError("");
          }}
          className="mt-10 w-full rounded-lg bg-blue-600 hover:bg-blue-700 p-3"
        >
          + New Chat
        </button>

        <div className="mt-10 text-gray-500 text-sm">
          Your AI Assistant
        </div>
      </aside>

      {/* Main Content */}
      <section className="flex-1 flex flex-col items-center px-5 py-10">

        <div className="w-full max-w-3xl">

          <div className="text-center mt-12 mb-12">
            <div className="text-5xl mb-5">✦</div>

            <h2 className="text-4xl font-bold">
              Welcome to Clause AI
            </h2>

            <p className="text-gray-400 mt-4">
              Ask questions about your documents
              and get intelligent AI-powered answers.
            </p>
          </div>

          {/* Question Input */}
          <div className="bg-gray-900 border border-gray-700 rounded-2xl p-4 shadow-xl">

            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask anything about your documents..."
              className="w-full bg-transparent outline-none resize-none h-28 text-white placeholder-gray-500"
            />

            <div className="flex justify-between items-center border-t border-gray-700 pt-4">

              <span className="text-xs text-gray-500">
                Powered by Clause AI
              </span>

              <button
                onClick={askQuestion}
                disabled={loading || !question.trim()}
                className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 rounded-lg px-6 py-2 font-medium"
              >
                {loading ? "Thinking..." : "Ask AI ↑"}
              </button>

            </div>
          </div>

          {/* Answer */}
          {answer && (
            <div className="mt-8 bg-gray-900 border border-gray-700 rounded-xl p-6">
              <h3 className="text-lg font-semibold text-blue-400 mb-4">
                ✦ AI Response
              </h3>

              <p className="text-gray-200 whitespace-pre-wrap leading-7">
                {answer}
              </p>
            </div>
          )}

          {/* Loading */}
          {loading && (
            <p className="text-center text-blue-400 mt-8">
              AI is thinking...
            </p>
          )}

          {/* Error */}
          {error && (
            <p className="text-red-400 mt-6 text-center">
              {error}
            </p>
          )}

        </div>
      </section>
    </main>
  );
}
