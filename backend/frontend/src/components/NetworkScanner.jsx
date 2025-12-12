export default function NetworkScanner({ message = "Scanning Network..." }) {
  return (
    <div className="fixed inset-0 bg-black/80 flex flex-col items-center justify-center z-50">

      {/* CÍRCULO RADAR */}
      <div className="relative w-64 h-64">
        
        {/* Anel externo */}
        <div className="absolute inset-0 rounded-full border-4 border-blue-500/30"></div>

        {/* Onda expansiva */}
        <div className="absolute inset-0 rounded-full border-4 border-blue-400 animate-ping opacity-70"></div>

        {/* Núcleo pulsante */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="w-10 h-10 bg-blue-500 rounded-full animate-pulse shadow-xl"></div>
        </div>

        {/* Linha do radar girando */}
        <div className="absolute inset-0 animate-spin-slow">
          <div className="absolute w-1/2 h-1 bg-blue-400 origin-left rounded-full opacity-70"></div>
        </div>
      </div>

      {/* TEXTO ANIMADO */}
      <p className="mt-8 text-blue-300 text-xl font-medium tracking-widest animate-pulse">
        {message}
      </p>

      {/* Linhas animadas estilo scanner */}
      <div className="mt-6 w-80 h-1 bg-gradient-to-r from-transparent via-blue-400 to-transparent animate-scan-line"></div>
    </div>
  );
}
