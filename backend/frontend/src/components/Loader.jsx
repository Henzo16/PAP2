export default function Loader({ message = "Aguarde..." }) {
  return (
    <div className="flex flex-col items-center justify-center py-10">
      <div className="relative flex items-center justify-center">
        {/* Círculo giratório */}
        <div className="w-14 h-14 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>

        {/* Pulsação interna */}
        <div className="absolute w-6 h-6 bg-blue-500 rounded-full animate-ping"></div>
      </div>

      <p className="mt-4 text-gray-700 text-lg font-medium animate-pulse">
        {message}
      </p>
    </div>
  );
}
