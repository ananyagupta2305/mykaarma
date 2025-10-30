// import React from "react";

// export default function ProductCard({ card, onToggleCompare, selected }) {
//   return (
//     <div
//       className={`border rounded-xl p-3 flex flex-col items-center shadow-md transition-all hover:shadow-lg ${
//         selected ? "border-blue-500 bg-blue-50" : "border-gray-200"
//       }`}
//     >
//       <h3 className="font-semibold text-lg text-gray-800 mb-1 text-center">
//         {card.name}
//       </h3>
//       <p className="text-gray-600 mb-2">{card.price}</p>

//       <button
//         onClick={onToggleCompare}
//         className={`px-3 py-1 rounded text-white ${
//           selected ? "bg-red-500" : "bg-blue-600 hover:bg-blue-700"
//         }`}
//       >
//         {selected ? "Selected" : "Compare"}
//       </button>
//     </div>
//   );
// }
import React from "react";

export default function ProductCard({ card, onToggleCompare, selected }) {
  return (
    <div
      className={`rounded-2xl p-4 text-center shadow-md border-2 transition-all duration-300 hover:scale-105 ${
        selected
          ? "border-blue-500 bg-blue-50"
          : "border-gray-200 bg-white hover:shadow-lg"
      }`}
    >
      <h3 className="font-semibold text-gray-900 text-lg truncate">{card.name}</h3>
      <p className="text-gray-600 text-sm mb-3">{card.price}</p>

      <button
        onClick={onToggleCompare}
        className={`w-full py-2 rounded-full text-sm font-medium transition-all ${
          selected
            ? "bg-blue-600 text-white shadow"
            : "bg-gray-200 hover:bg-blue-100 text-gray-800"
        }`}
      >
        {selected ? "Selected ✓" : "Select"}
      </button>
    </div>
  );
}
