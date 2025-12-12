import { useState } from "react";
import NetworkScanner from "../components/NetworkScanner";
import { API_URL } from "../config";
import { useNavigate } from "react-router-dom";

export default function DetectRouterPage() {
  const [scanning, setScanning] = useState(false);
  const [result, setResult] = useState(null);
  const navigate = useNavigate();

  async function detectRouter() {
    setScanning(true);
    setResult(null);

    try {
      const res = await fetch(`${API_URL}/router/auto-detect?username=admin&password=cisco`);
      const data = await res.json();
      setResult(data);
    } catch {
      setResult({ error: "Erro ao comunicar com o servidor." });
    }

    setScanning(false);
  }

  return (
    <div className="p-6 max-w-xl mx-auto">

      {scanning && <NetworkScanner message="Detectando Roteador..." />}

      <h1 className="text-2xl font-bold mb-6 text-gray-800">
        Auto-Detecção de Roteador
      </h1>

      <button
        onClick={detectRouter}
        className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-3 rounded-lg"
      >
        Detectar Roteador
      </button>

      {result && (
        <div className="mt-8 bg-white p-4 shadow rounded-lg">
          {result.error && (
            <p className="text-red-600 font-medium">{result.error}</p>
          )}

          {result.detected === false && (
            <p className="text-yellow-600 font-medium">
              ⚠ Nenhum roteador encontrado. Verifique conexões e credenciais.
            </p>
          )}

          {result.detected === true && (
            <div>
              <p className="text-green-600 font-bold text-lg">✔ Roteador Detectado!</p>
              <p><strong>Modelo:</strong> {result.model}</p>
              <p><strong>IP:</strong> {result.ip}</p>

              <button
                className="mt-4 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg"
                onClick={() => navigate("/router/services")}
              >
                Configurar Serviços →
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
