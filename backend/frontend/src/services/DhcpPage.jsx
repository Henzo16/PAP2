import { useEffect, useState } from "react";
import { API_URL } from "../config";
import { useNavigate } from "react-router-dom";

export default function DhcpPage() {
  const navigate = useNavigate();

  const routerInfo = JSON.parse(localStorage.getItem("detectedRouter"));
  const token = localStorage.getItem("token");

  const [dhcps, setDhcps] = useState([]);
  const [loading, setLoading] = useState(false);

  const [form, setForm] = useState({
    router_id: routerInfo?.id,
    pool_name: "",
    network: "",
    mask: "",
    gateway: "",
  });

  const [editingId, setEditingId] = useState(null);

  // ------------------------------------
  // Buscar DHCPs existentes
  // ------------------------------------
  async function fetchDhcp() {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/dhcp/${routerInfo.id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await res.json();
      setDhcps(data);
    } catch (err) {
      console.error("Erro ao carregar DHCP:", err);
    }
    setLoading(false);
  }

  useEffect(() => {
    fetchDhcp();
  }, []);

  // ------------------------------------
  // Criar ou Atualizar DHCP
  // ------------------------------------
  async function handleSubmit(e) {
    e.preventDefault();

    const url = editingId
      ? `${API_URL}/dhcp/${editingId}`
      : `${API_URL}/dhcp`;

    const method = editingId ? "PUT" : "POST";

    try {
      const res = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(form),
      });

      if (!res.ok) {
        alert("Erro ao salvar configuração DHCP.");
        return;
      }

      // Limpar
      setForm({
        router_id: routerInfo.id,
        pool_name: "",
        network: "",
        mask: "",
        gateway: "",
      });

      setEditingId(null);
      fetchDhcp();
    } catch (err) {
      console.error(err);
      alert("Erro ao conectar ao servidor.");
    }
  }

  // ------------------------------------
  // Apagar DHCP
  // ------------------------------------
  async function handleDelete(id) {
    if (!confirm("Tem certeza que deseja remover esta configuração DHCP?")) return;

    try {
      const res = await fetch(`${API_URL}/dhcp/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });

      if (res.ok) fetchDhcp();
    } catch (err) {
      alert("Erro ao remover DHCP.");
    }
  }

  // ------------------------------------
  // Editar DHCP
  // ------------------------------------
  function editDhcp(d) {
    setEditingId(d.id);
    setForm({
      router_id: routerInfo.id,
      pool_name: d.pool_name,
      network: d.network,
      mask: d.mask,
      gateway: d.gateway,
    });
  }

  return (
    <div className="min-h-screen bg-gray-100 p-6 flex justify-center">
      <div className="w-full max-w-4xl bg-white rounded-xl shadow-xl p-8">
        <h1 className="text-3xl font-bold text-gray-800 text-center mb-6">
          Configuração DHCP 🟦
        </h1>

        {/* FORMULÁRIO */}
        <form className="grid grid-cols-1 sm:grid-cols-2 gap-4" onSubmit={handleSubmit}>
          
          <input
            className="p-3 border rounded-lg"
            placeholder="Nome do Pool"
            value={form.pool_name}
            onChange={(e) => setForm({ ...form, pool_name: e.target.value })}
            required
          />

          <input
            className="p-3 border rounded-lg"
            placeholder="Rede (ex: 192.168.1.0)"
            value={form.network}
            onChange={(e) => setForm({ ...form, network: e.target.value })}
            required
          />

          <input
            className="p-3 border rounded-lg"
            placeholder="Máscara (ex: 255.255.255.0)"
            value={form.mask}
            onChange={(e) => setForm({ ...form, mask: e.target.value })}
            required
          />

          <input
            className="p-3 border rounded-lg"
            placeholder="Gateway (opcional)"
            value={form.gateway}
            onChange={(e) => setForm({ ...form, gateway: e.target.value })}
          />

          <button
            type="submit"
            className="col-span-full bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg font-medium transition"
          >
            {editingId ? "Atualizar DHCP" : "Criar DHCP"}
          </button>
        </form>

        <hr className="my-8" />

        {/* LISTA DHCP */}
        <h2 className="text-2xl font-semibold mb-4">Configurações Existentes</h2>

        {loading ? (
          <p>Carregando...</p>
        ) : dhcps.length === 0 ? (
          <p className="text-gray-500">Nenhuma configuração DHCP encontrada.</p>
        ) : (
          <ul className="space-y-4">
            {dhcps.map((d) => (
              <li key={d.id} className="p-4 border rounded-lg flex justify-between items-center">
                <div>
                  <p><strong>Pool:</strong> {d.pool_name}</p>
                  <p><strong>Rede:</strong> {d.network} / {d.mask}</p>
                  {d.gateway && <p><strong>Gateway:</strong> {d.gateway}</p>}
                </div>

                <div className="flex gap-2">
                  <button
                    className="px-3 py-1 bg-yellow-500 text-white rounded-lg"
                    onClick={() => editDhcp(d)}
                  >
                    Editar
                  </button>

                  <button
                    className="px-3 py-1 bg-red-600 text-white rounded-lg"
                    onClick={() => handleDelete(d.id)}
                  >
                    Remover
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}

        {/* VOLTAR */}
        <button
          className="mt-10 w-full bg-gray-300 hover:bg-gray-400 text-gray-800 p-3 rounded-xl transition"
          onClick={() => navigate("/services")}
        >
          Voltar aos Serviços
        </button>
      </div>
    </div>
  );
}
