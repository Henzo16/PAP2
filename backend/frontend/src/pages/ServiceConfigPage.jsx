import { useNavigate } from "react-router-dom";
import { useEffect } from "react";

export default function ServiceConfigPage() {
  const navigate = useNavigate();

  // Buscar o roteador que foi detectado
  const routerInfo = JSON.parse(localStorage.getItem("detectedRouter"));

  useEffect(() => {
    if (!routerInfo) {
      alert("Nenhum roteador detectado! Volte e tente novamente.");
      navigate("/detect-router");
    }
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 flex justify-center p-6">
      <div className="w-full max-w-3xl bg-white shadow-xl rounded-xl p-8">
        <h1 className="text-3xl font-bold text-gray-800 text-center mb-3">
          Serviços Disponíveis ⚙️
        </h1>

        <p className="text-center text-gray-600 mb-6">
          Roteador detectado:{" "}
          <span className="font-semibold text-blue-600">
            {routerInfo?.model || "Desconhecido"}
          </span>
          <br />
          IP:{" "}
          <span className="font-semibold text-blue-600">
            {routerInfo?.ip || "N/A"}
          </span>
        </p>

        {/* Botões dos serviços */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <button
            className="p-4 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-medium shadow-md transition"
            onClick={() => navigate("/services/dhcp")}
          >
            DHCP
          </button>

          <button
            className="p-4 bg-green-600 hover:bg-green-700 text-white rounded-xl font-medium shadow-md transition"
            disabled
          >
            NAT (em breve)
          </button>

          <button
            className="p-4 bg-purple-600 hover:bg-purple-700 text-white rounded-xl font-medium shadow-md transition"
            disabled
          >
            VLAN (em breve)
          </button>

          <button
            className="p-4 bg-orange-600 hover:bg-orange-700 text-white rounded-xl font-medium shadow-md transition"
            disabled
          >
            ACL (em breve)
          </button>
        </div>

        {/* Voltar */}
        <button
          className="mt-10 w-full bg-gray-300 hover:bg-gray-400 text-gray-800 p-3 rounded-xl transition"
          onClick={() => navigate("/dashboard")}
        >
          Voltar ao Dashboard
        </button>
      </div>
    </div>
  );
}


