import { useState } from "react";
import { API_URL } from "../config";
import { useNavigate } from "react-router-dom";

export default function DetectRouterPage() {
  const navigate = useNavigate();

  const [ip, setIp] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState("");

  const detectRouter = async () => {
    setLoading(true);
    setErro("");

    const token = localStorage.getItem("token");

    try {
      const res = await fetch(
        `${API_URL}/router/auto-detect?ip=${ip}&username=${username}&password=${password}`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await res.json();

      // ⚠️ Se a request falhou → Não avança
      if (!res.ok) {
        setErro(data.detail || "Erro ao tentar detectar o roteador.");
        setLoading(false);
        return;
      }

      // ⚠️ Se o backend disser detected: false → Não avança
      if (!data.detected) {
        setErro(data.detail || "Nenhum roteador encontrado.");
        setLoading(false);
        return;
      }

      // ✔️ Roteador REALMENTE detectado
      localStorage.setItem("router_info", JSON.stringify(data));
      navigate("/router/services");

    } catch (err) {
      setErro("Erro ao comunicar com o servidor.");
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col items-center justify-center p-6 text-white">

      {loading && (
        <div className="fixed inset-0 bg-black bg-opacity-80 flex flex-col items-center justify-center z-50">
          <div className="animate-pulse text-blue-400 text-3xl font-bold tracking-wide">
            SCANNING NETWORK…
          </div>

          <div className="mt-6 w-24 h-24 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>

          <p className="mt-4 text-gray-300 text-lg">
            Tentando detectar roteador Cisco...
          </p>
        </div>
      )}

      <div className="bg-gray-800 p-8 rounded-xl shadow-2xl w-full max-w-md border border-gray-700">
        <h1 className="text-3xl font-bold text-center text-blue-400 mb-6">
          Detectar Roteador Cisco
        </h1>

        {erro && (
          <p className="bg-red-600 text-white p-3 rounded-lg mb-4 text-center">
            {erro}
          </p>
        )}

        <div className="space-y-4">
          <input
            type="text"
            placeholder="Endereço IP"
            className="w-full p-3 bg-gray-700 text-white border border-gray-600 rounded-lg"
            value={ip}
            onChange={(e) => setIp(e.target.value)}
          />

          <input
            type="text"
            placeholder="Username"
            className="w-full p-3 bg-gray-700 text-white border border-gray-600 rounded-lg"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />

          <input
            type="password"
            placeholder="Password"
            className="w-full p-3 bg-gray-700 text-white border border-gray-600 rounded-lg"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button
            onClick={detectRouter}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-semibold tracking-wide transition"
          >
            DETECTAR ROTEADOR
          </button>
        </div>
      </div>
    </div>
  );
}
