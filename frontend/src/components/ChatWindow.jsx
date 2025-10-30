// // import React, { useState } from "react";

// // const ChatWindow = () => {
// //   const [messages, setMessages] = useState([
// //     { sender: "bot", text: "Hi — ask me about phones (e.g., 'Best camera phone under ₹30,000?')" },
// //   ]);
// //   const [input, setInput] = useState("");
// //   const [cards, setCards] = useState([]);
// //   const [selectedPhones, setSelectedPhones] = useState([]);
// //   const [comparison, setComparison] = useState(null);

// //   // Helper: clean formatting for nested fields
// //   const formatValue = (val) => {
// //     if (val === null || val === undefined) return "—";
// //     if (typeof val === "object") {
// //       if (val.main || val.ultra_wide || val.capacity_mah) {
// //         return Object.entries(val)
// //           .map(([key, value]) => {
// //             if (value === null || value === false) return null;
// //             if (typeof value === "boolean") return `${key}: ${value ? "Yes" : "No"}`;
// //             return `${key}: ${value}`;
// //           })
// //           .filter(Boolean)
// //           .join(", ");
// //       }
// //       return JSON.stringify(val);
// //     }
// //     return String(val);
// //   };

// //   const sendMessage = async () => {
// //     if (!input.trim()) return;

// //     const userMessage = { sender: "user", text: input };
// //     setMessages((prev) => [...prev, userMessage]);
// //     setInput("");

// //     try {
// //       const res = await fetch("http://127.0.0.1:8000/chat", {
// //         method: "POST",
// //         headers: { "Content-Type": "application/json" },
// //         body: JSON.stringify({ message: input }),
// //       });

// //       const data = await res.json();
// //       console.log("💬 Chat API response:", data);

// //       if (data.text) {
// //         setMessages((prev) => [...prev, { sender: "bot", text: data.text }]);
// //       }

// //       if (data.cards) {
// //         setCards(data.cards);
// //         setSelectedPhones([]);
// //         setComparison(null);
// //       }

// //       // handle direct comparison or unwrapped structure
// //       if (data.comparison) {
// //         console.log("✅ Setting comparison (wrapped):", data.comparison);
// //         setComparison(data.comparison);
// //         setMessages((prev) => [...prev, { sender: "bot", text: "Here’s the comparison below:" }]);
// //       } else if (data.title && data.names) {
// //         console.log("✅ Setting comparison (unwrapped):", data);
// //         setComparison(data);
// //         setMessages((prev) => [...prev, { sender: "bot", text: "Here’s the comparison below:" }]);
// //       }
// //     } catch (error) {
// //       console.error("❌ Error contacting backend:", error);
// //       setMessages((prev) => [...prev, { sender: "bot", text: "Error contacting backend." }]);
// //     }
// //   };

// //   const handleSelect = (id) => {
// //     setSelectedPhones((prev) =>
// //       prev.includes(id) ? prev.filter((p) => p !== id) : [...prev, id]
// //     );
// //   };

// //   const handleCompare = async () => {
// //     if (selectedPhones.length < 2) {
// //       alert("Select at least 2 phones to compare!");
// //       return;
// //     }

// //     try {
// //       const res = await fetch("http://127.0.0.1:8000/compare", {
// //         method: "POST",
// //         headers: { "Content-Type": "application/json" },
// //         body: JSON.stringify({ phones: selectedPhones }),
// //       });
// //       const data = await res.json();
// //       console.log("📊 Compare API response:", data);

// //       // Accept both wrapped or unwrapped comparison JSON
// //       if (data.comparison) setComparison(data.comparison);
// //       else setComparison(data);

// //       setMessages((prev) => [...prev, { sender: "bot", text: "Here’s the comparison below:" }]);
// //     } catch (error) {
// //       console.error("❌ Comparison error:", error);
// //     }
// //   };

// //   console.log("🧩 Current comparison state:", comparison);

// //   return (
// //     <div className="flex flex-col items-center w-full min-h-screen bg-gray-100 p-4">
// //       <h1 className="text-2xl font-bold mb-4">📱 Phone Recommender Chatbot</h1>

// //       {/* Chat Area */}
// //       <div className="w-full max-w-lg bg-white rounded-2xl shadow p-4 mb-4 overflow-y-auto max-h-[60vh]">
// //         {messages.map((msg, idx) => (
// //           <div
// //             key={idx}
// //             className={`my-2 p-2 rounded-xl ${
// //               msg.sender === "user" ? "bg-blue-100 text-right" : "bg-gray-200 text-left"
// //             }`}
// //           >
// //             {msg.text}
// //           </div>
// //         ))}

// //         {/* Product Cards */}
// //         {cards.length > 0 && (
// //           <div className="grid grid-cols-2 gap-4 mt-4">
// //             {cards.map((card) => (
// //               <div
// //                 key={card.id}
// //                 className={`border rounded-xl p-3 shadow text-center transition-all ${
// //                   selectedPhones.includes(card.id)
// //                     ? "bg-blue-100 border-blue-400"
// //                     : "bg-white border-gray-300"
// //                 }`}
// //               >
// //                 <h2 className="font-semibold">{card.name}</h2>
// //                 <p className="text-gray-600">{card.price}</p>
// //                 <button
// //                   onClick={() => handleSelect(card.id)}
// //                   className={`mt-2 px-3 py-1 text-sm rounded-full ${
// //                     selectedPhones.includes(card.id)
// //                       ? "bg-blue-600 text-white"
// //                       : "bg-gray-300 text-black"
// //                   }`}
// //                 >
// //                   {selectedPhones.includes(card.id) ? "Selected" : "Select"}
// //                 </button>
// //               </div>
// //             ))}
// //           </div>
// //         )}

// //         {/* Compare Button */}
// //         {cards.length > 0 && (
// //           <div className="mt-4 text-center">
// //             <button
// //               onClick={handleCompare}
// //               className="px-4 py-2 bg-green-600 text-white rounded-lg"
// //             >
// //               Compare Selected ({selectedPhones.length})
// //             </button>
// //           </div>
// //         )}

// //         {/* Comparison Section */}
// //         {comparison ? (
// //           <div className="mt-6 bg-white border-2 border-red-500 rounded-xl p-4 shadow">
// //             <h3 className="text-lg font-semibold mb-2">
// //               {comparison.title || "Comparison Table"}
// //             </h3>

// //             {comparison.specs ? (
// //               <>
// //                 <table className="w-full text-sm border-collapse border border-gray-300">
// //                   <thead>
// //                     <tr>
// //                       <th className="border border-gray-300 p-2 text-left">Spec</th>
// //                       {comparison.names.map((name, idx) => (
// //                         <th key={idx} className="border border-gray-300 p-2 text-left">
// //                           {name}
// //                         </th>
// //                       ))}
// //                     </tr>
// //                   </thead>
// //                   <tbody>
// //                     {Object.keys(comparison.specs).map((spec, i) => (
// //                       <tr key={i}>
// //                         <td className="border border-gray-300 p-2 font-medium">{spec}</td>
// //                         {comparison.specs[spec].map((val, j) => (
// //                           <td key={j} className="border border-gray-300 p-2">
// //                             {formatValue(val)}
// //                           </td>
// //                         ))}
// //                       </tr>
// //                     ))}
// //                   </tbody>
// //                 </table>

// //                 {comparison.rationales && (
// //                   <div className="mt-4">
// //                     <h4 className="font-semibold text-gray-800 mb-2">Why Recommended</h4>
// //                     <ul className="text-gray-700 text-sm space-y-1">
// //                       {comparison.names.map((name, idx) => (
// //                         <li key={idx}>
// //                           <strong>{name}:</strong> {comparison.rationales[idx]}
// //                         </li>
// //                       ))}
// //                     </ul>
// //                   </div>
// //                 )}
// //               </>
// //             ) : (
// //               <pre className="bg-gray-900 text-green-400 text-xs p-3 rounded">
// //                 {JSON.stringify(comparison, null, 2)}
// //               </pre>
// //             )}
// //           </div>
// //         ) : (
// //           <p className="text-gray-500 text-sm mt-4">No comparison data yet.</p>
// //         )}
// //       </div>

// //       {/* Input Bar */}
// //       <div className="flex w-full max-w-lg mt-auto">
// //         <input
// //           className="flex-1 border border-gray-300 rounded-l-xl p-2 focus:outline-none"
// //           placeholder="Ask about phones..."
// //           value={input}
// //           onChange={(e) => setInput(e.target.value)}
// //           onKeyDown={(e) => e.key === "Enter" && sendMessage()}
// //         />
// //         <button
// //           onClick={sendMessage}
// //           className="bg-blue-600 text-white px-4 rounded-r-xl"
// //         >
// //           Send
// //         </button>
// //       </div>
// //     </div>
// //   );
// // };

// // export default ChatWindow;




// import React, { useState } from "react";

// const ChatWindow = () => {
//   const [messages, setMessages] = useState([
//     { sender: "bot", text: "👋 Hi! Ask me about phones — e.g., 'Best camera phone under ₹30,000?'" },
//   ]);
//   const [input, setInput] = useState("");
//   const [cards, setCards] = useState([]);
//   const [selectedPhones, setSelectedPhones] = useState([]);
//   const [comparison, setComparison] = useState(null);

//   const formatValue = (val) => {
//     if (val === null || val === undefined) return "—";
//     if (typeof val === "object") {
//       return Object.entries(val)
//         .map(([key, value]) => `${key}: ${value}`)
//         .join(", ");
//     }
//     return String(val);
//   };

//   const sendMessage = async () => {
//     if (!input.trim()) return;
//     const userMessage = { sender: "user", text: input };
//     setMessages((prev) => [...prev, userMessage]);
//     setInput("");

//     try {
//       const res = await fetch("http://127.0.0.1:8000/chat", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ message: input }),
//       });

//       const data = await res.json();
//       if (data.text) setMessages((prev) => [...prev, { sender: "bot", text: data.text }]);
//       if (data.cards) {
//         setCards(data.cards);
//         setSelectedPhones([]);
//         setComparison(null);
//       }
//       if (data.comparison) setComparison(data.comparison);
//     } catch (error) {
//       setMessages((prev) => [...prev, { sender: "bot", text: "⚠️ Error contacting backend." }]);
//     }
//   };

//   const handleSelect = (id) => {
//     setSelectedPhones((prev) =>
//       prev.includes(id) ? prev.filter((p) => p !== id) : [...prev, id]
//     );
//   };

//   const handleCompare = async () => {
//     if (selectedPhones.length < 2) {
//       alert("Select at least 2 phones to compare!");
//       return;
//     }

//     try {
//       const res = await fetch("http://127.0.0.1:8000/compare", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ phones: selectedPhones }),
//       });

//       const data = await res.json();
//       setComparison(data);
//       setMessages((prev) => [...prev, { sender: "bot", text: "Here’s the comparison below:" }]);
//     } catch (error) {
//       console.error(error);
//     }
//   };

//   return (
//     <div className="flex flex-col items-center w-full min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 p-6">
//       <h1 className="text-3xl font-bold mb-6 text-blue-700">
//         📱 Smart Phone Recommender
//       </h1>

//       {/* Chat area */}
//       <div className="w-full max-w-2xl bg-white rounded-2xl shadow-xl p-6 mb-6 overflow-y-auto max-h-[65vh] border border-gray-200">
//         {messages.map((msg, idx) => (
//           <div
//             key={idx}
//             className={`my-3 p-3 rounded-xl text-sm md:text-base transition-all ${
//               msg.sender === "user"
//                 ? "bg-blue-100 text-right ml-auto w-fit max-w-[80%]"
//                 : "bg-gray-100 text-left mr-auto w-fit max-w-[80%]"
//             }`}
//           >
//             {msg.text}
//           </div>
//         ))}

//         {/* Product cards */}
//         {cards.length > 0 && (
//           <>
//             <h2 className="mt-6 mb-3 font-semibold text-gray-700">
//               📦 Recommended Phones
//             </h2>
//             <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
//               {cards.map((card) => (
//                 <div
//                   key={card.id}
//                   className={`relative border rounded-xl p-4 shadow-sm hover:shadow-md transition-all transform hover:-translate-y-1 ${
//                     selectedPhones.includes(card.id)
//                       ? "border-blue-500 bg-blue-50"
//                       : "border-gray-200 bg-white"
//                   }`}
//                 >
//                   <h3 className="font-semibold text-gray-800 truncate">{card.name}</h3>
//                   <p className="text-gray-600 text-sm mt-1">{card.price}</p>

//                   <button
//                     onClick={() => handleSelect(card.id)}
//                     className={`mt-3 px-3 py-1.5 w-full text-sm rounded-lg font-medium transition ${
//                       selectedPhones.includes(card.id)
//                         ? "bg-blue-600 text-white"
//                         : "bg-gray-200 hover:bg-blue-100 text-gray-800"
//                     }`}
//                   >
//                     {selectedPhones.includes(card.id) ? "Selected ✓" : "Select"}
//                   </button>
//                 </div>
//               ))}
//             </div>

//             {/* Compare Button */}
//             <div className="mt-5 text-center">
//               <button
//                 onClick={handleCompare}
//                 className="px-5 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg shadow transition"
//               >
//                 Compare Selected ({selectedPhones.length})
//               </button>
//             </div>
//           </>
//         )}

//         {/* Comparison Section */}
//         {comparison && (
//           <div className="mt-8 bg-white border border-gray-300 rounded-xl p-5 shadow">
//             <h3 className="text-lg font-semibold mb-3 text-blue-700">
//               {comparison.title || "📊 Comparison Table"}
//             </h3>

//             <div className="overflow-x-auto">
//               <table className="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
//                 <thead className="bg-gray-50">
//                   <tr>
//                     <th className="border border-gray-200 p-2 text-left">Spec</th>
//                     {comparison.names.map((name, idx) => (
//                       <th
//                         key={idx}
//                         className="border border-gray-200 p-2 text-left text-gray-700"
//                       >
//                         {name}
//                       </th>
//                     ))}
//                   </tr>
//                 </thead>
//                 <tbody>
//                   {Object.keys(comparison.specs).map((spec, i) => (
//                     <tr key={i} className="hover:bg-gray-50">
//                       <td className="border border-gray-200 p-2 font-medium text-gray-700">
//                         {spec}
//                       </td>
//                       {comparison.specs[spec].map((val, j) => (
//                         <td key={j} className="border border-gray-200 p-2 text-gray-600">
//                           {formatValue(val)}
//                         </td>
//                       ))}
//                     </tr>
//                   ))}
//                 </tbody>
//               </table>
//             </div>

//             {/* Why Recommended */}
//             {comparison.rationales && (
//               <div className="mt-5 bg-blue-50 p-3 rounded-lg">
//                 <h4 className="font-semibold text-blue-800 mb-2">
//                   💡 Why Recommended
//                 </h4>
//                 <ul className="text-gray-700 text-sm space-y-1">
//                   {comparison.names.map((name, idx) => (
//                     <li key={idx}>
//                       <strong>{name}:</strong> {comparison.rationales[idx]}
//                     </li>
//                   ))}
//                 </ul>
//               </div>
//             )}
//           </div>
//         )}
//       </div>

//       {/* Input bar */}
//       <div className="flex w-full max-w-2xl mt-auto">
//         <input
//           className="flex-1 border border-gray-300 rounded-l-xl p-3 focus:outline-none focus:ring-2 focus:ring-blue-400"
//           placeholder="Ask about phones..."
//           value={input}
//           onChange={(e) => setInput(e.target.value)}
//           onKeyDown={(e) => e.key === "Enter" && sendMessage()}
//         />
//         <button
//           onClick={sendMessage}
//           className="bg-blue-600 hover:bg-blue-700 text-white px-5 rounded-r-xl transition"
//         >
//           Send
//         </button>
//       </div>
//     </div>
//   );
// };

// export default ChatWindow;
import React, { useState } from "react";
import ComparisonTable from "./CompareTable";
import ProductCard from "./ProductCard";

const ChatWindow = () => {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "👋 Hi! I'm your Smart Phone Assistant — ask me anything like 'Best camera phone under ₹30,000?'" },
  ]);
  const [input, setInput] = useState("");
  const [cards, setCards] = useState([]);
  const [selectedPhones, setSelectedPhones] = useState([]);
  const [comparison, setComparison] = useState(null);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      const data = await res.json();
      if (data.text) setMessages((prev) => [...prev, { sender: "bot", text: data.text }]);
      if (data.cards) {
        setCards(data.cards);
        setSelectedPhones([]);
        setComparison(null);
      }
      if (data.comparison) setComparison(data.comparison);
    } catch {
      setMessages((prev) => [...prev, { sender: "bot", text: "⚠️ Sorry, I couldn’t connect to the server." }]);
    }
  };

  const handleSelect = (id) => {
    setSelectedPhones((prev) =>
      prev.includes(id) ? prev.filter((p) => p !== id) : [...prev, id]
    );
  };

  const handleCompare = async () => {
    if (selectedPhones.length < 2) {
      alert("Please select at least 2 phones to compare!");
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:8000/compare", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ phones: selectedPhones }),
      });
      const data = await res.json();
      setComparison(data);
      setMessages((prev) => [...prev, { sender: "bot", text: "📊 Here’s your detailed comparison:" }]);
    } catch {
      setMessages((prev) => [...prev, { sender: "bot", text: "⚠️ Comparison failed. Please try again." }]);
    }
  };

  return (
    <div className="flex flex-col items-center w-full min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-6">
      <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600 mb-6 drop-shadow-sm">
        📱 Smart Phone Recommender
      </h1>

      {/* Chat area */}
      <div className="w-full max-w-3xl bg-white/90 backdrop-blur-sm border border-gray-200 rounded-3xl shadow-xl p-6 overflow-y-auto max-h-[70vh]">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`my-3 flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`p-3 rounded-2xl max-w-[80%] shadow-sm transition-all ${
                msg.sender === "user"
                  ? "bg-gradient-to-r from-blue-600 to-indigo-600 text-white"
                  : "bg-gray-100 text-gray-800"
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}

        {/* Product cards */}
        {cards.length > 0 && (
          <div className="mt-6">
            <h2 className="font-semibold text-gray-800 mb-3 text-lg">
              🔍 Recommended Phones
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
              {cards.map((card) => (
                <ProductCard
                  key={card.id}
                  card={card}
                  onToggleCompare={() => handleSelect(card.id)}
                  selected={selectedPhones.includes(card.id)}
                />
              ))}
            </div>
            <div className="mt-5 text-center">
              <button
                onClick={handleCompare}
                className="px-5 py-2.5 bg-gradient-to-r from-green-500 to-emerald-600 text-white font-medium rounded-lg shadow-md hover:scale-105 transition-transform"
              >
                Compare Selected ({selectedPhones.length})
              </button>
            </div>
          </div>
        )}

        {/* Comparison section */}
        {comparison && (
          <div className="mt-8">
            <ComparisonTable data={comparison} />
          </div>
        )}
      </div>

      {/* Input area */}
      <div className="flex w-full max-w-3xl mt-5 bg-white rounded-full shadow-lg border border-gray-200 overflow-hidden">
        <input
          className="flex-1 p-3 px-5 focus:outline-none text-gray-800"
          placeholder="Ask me about phones (e.g., 'Compare iPhone 15 vs Pixel 8')..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button
          onClick={sendMessage}
          className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white px-6 font-semibold transition-all"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatWindow;
