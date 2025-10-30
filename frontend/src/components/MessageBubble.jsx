import React from "react";
import CompareTable from "./CompareTable";

export default function MessageBubble({ from, text, comparison }) {
  return (
    <div
      className={`my-2 ${
        from === "user" ? "text-right" : "text-left"
      }`}
    >
      <div
        className={`inline-block px-4 py-2 rounded-lg ${
          from === "user"
            ? "bg-green-200 text-gray-800"
            : "bg-gray-100 text-gray-900"
        }`}
      >
        {text}
      </div>

      {/* Render comparison table if present */}
      {comparison && (
        <div className="mt-2">
          <CompareTable data={comparison} />
        </div>
      )}
    </div>
  );
}
