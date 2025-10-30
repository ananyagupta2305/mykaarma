// import React from "react";
// import { CheckCircle, Battery, Camera, Cpu, Smartphone, HardDrive } from "lucide-react";

// function ComparisonTable({ data }) {
//   if (!data || !data.names) return null;

//   const { title, names, specs, rationales } = data;

//   // --- Helper: Format nested objects (Camera, Battery)
//   const formatValue = (val) => {
//     if (val === null || val === undefined) return "—";
//     if (typeof val === "object") {
//       if (val.main || val.ultra_wide || val.capacity_mah) {
//         return Object.entries(val)
//           .map(([k, v]) => (v ? `${k}: ${v}` : null))
//           .filter(Boolean)
//           .join(", ");
//       }
//       return JSON.stringify(val);
//     }
//     return String(val);
//   };

//   // --- Highlight best numeric values automatically
//   const getHighlightIndices = (specArray, specName) => {
//     let numericValues = specArray.map((v) => {
//       if (typeof v === "object") {
//         if (v.capacity_mah) return v.capacity_mah;
//         if (v.main && v.main.includes("MP")) return parseInt(v.main);
//       }
//       if (typeof v === "string" && v.match(/\d+/)) {
//         return parseInt(v.match(/\d+/)[0]);
//       }
//       return 0;
//     });

//     const maxVal = Math.max(...numericValues);
//     return numericValues.map((n) => n === maxVal);
//   };

//   return (
//     <div className="mt-6 bg-white p-6 rounded-2xl shadow-lg border border-gray-200">
//       <h3 className="text-2xl font-semibold mb-6 text-gray-800 flex items-center gap-2">
//         <Smartphone className="text-blue-600" size={22} /> {title}
//       </h3>

//       {/* Table */}
//       <div className="overflow-x-auto rounded-xl border border-gray-200">
//         <table className="min-w-full border-collapse text-sm">
//           <thead className="bg-blue-50">
//             <tr>
//               <th className="border px-3 py-2 text-left font-semibold text-gray-800">Spec</th>
//               {names.map((name, idx) => (
//                 <th key={idx} className="border px-3 py-2 text-left font-semibold text-gray-800">
//                   {name}
//                 </th>
//               ))}
//             </tr>
//           </thead>

//           <tbody>
//             {Object.keys(specs).map((spec, i) => {
//               const highlightFlags = getHighlightIndices(specs[spec], spec);
//               return (
//                 <tr
//                   key={i}
//                   className={i % 2 === 0 ? "bg-white" : "bg-gray-50 hover:bg-gray-100 transition-all"}
//                 >
//                   <td className="border px-3 py-2 font-medium text-gray-700">{spec}</td>
//                   {specs[spec].map((val, j) => (
//                     <td
//                       key={j}
//                       className={`border px-3 py-2 ${
//                         highlightFlags[j]
//                           ? "bg-green-50 font-semibold text-green-700"
//                           : "text-gray-700"
//                       }`}
//                     >
//                       {formatValue(val)}
//                     </td>
//                   ))}
//                 </tr>
//               );
//             })}
//           </tbody>
//         </table>
//       </div>

//       {/* Rationales Section */}
//       <div className="mt-6 bg-gray-50 rounded-xl p-4 border border-gray-200">
//         <h4 className="font-semibold text-lg mb-2 flex items-center gap-2">
//           <CheckCircle className="text-green-600" size={18} /> Why Recommended
//         </h4>
//         <ul className="space-y-1 text-gray-700 text-sm">
//           {rationales.map((r, i) => (
//             <li key={i} className="leading-snug">
//               <span className="font-semibold text-gray-800">{names[i]}:</span> {r}
//             </li>
//           ))}
//         </ul>
//       </div>
//     </div>
//   );
// }

// export default ComparisonTable;
import React from "react";
import { CheckCircle, Smartphone } from "lucide-react";

export default function ComparisonTable({ data }) {
  if (!data || !data.names) return null;
  const { title, names, specs, rationales } = data;

  const formatValue = (val) => {
    if (val === null || val === undefined) return "—";
    if (typeof val === "object")
      return Object.entries(val)
        .map(([k, v]) => `${k}: ${v}`)
        .join(", ");
    return String(val);
  };

  return (
    <div className="bg-white rounded-2xl border border-gray-200 shadow-lg p-5">
      <h3 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
        <Smartphone className="text-blue-600" /> {title || "Comparison Table"}
      </h3>

      <div className="overflow-x-auto rounded-xl border border-gray-200">
        <table className="min-w-full border-collapse text-sm">
          <thead className="bg-gradient-to-r from-blue-50 to-indigo-50">
            <tr>
              <th className="p-3 border border-gray-200 text-left text-gray-700 font-semibold">
                Spec
              </th>
              {names.map((name, i) => (
                <th key={i} className="p-3 border border-gray-200 text-left text-gray-700 font-semibold">
                  {name}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {Object.keys(specs).map((spec, idx) => (
              <tr
                key={idx}
                className={idx % 2 === 0 ? "bg-white" : "bg-gray-50 hover:bg-gray-100"}
              >
                <td className="p-3 border border-gray-200 font-medium text-gray-800">
                  {spec}
                </td>
                {specs[spec].map((val, j) => (
                  <td key={j} className="p-3 border border-gray-200 text-gray-700">
                    {formatValue(val)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {rationales && (
        <div className="mt-5 bg-blue-50 p-4 rounded-xl border border-blue-100">
          <h4 className="font-semibold text-blue-800 mb-2 flex items-center gap-2">
            <CheckCircle className="text-green-600" size={18} /> Why Recommended
          </h4>
          <ul className="text-gray-700 text-sm space-y-1">
            {rationales.map((r, i) => (
              <li key={i}>
                <strong className="text-gray-900">{names[i]}:</strong> {r}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
