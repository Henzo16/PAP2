export default function Input({ label, type = "text", value, onChange }) {
  return (
    <div className="mb-4">
      <label className="block text-gray-300 text-sm mb-1">{label}</label>
      <input
        type={type}
        value={value}
        onChange={onChange}
        className="w-full px-3 py-2 rounded bg-gray-800 border border-gray-700 text-white focus:outline-none focus:border-blue-500 transition"
      />
    </div>
  );
}
