import DashboardLayout from "../components/DashboardLayout";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  const token = localStorage.getItem("token");

  useEffect(() => {
    async function loadUser() {
      const res = await fetch("http://127.0.0.1:8000/api/auth/me", {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!res.ok) return navigate("/login");

      const data = await res.json();
      setUser(data);
    }
    loadUser();
  }, []);

  if (!user) return <p className="p-10 text-gray-500">Carregando...</p>;

  return (
    <DashboardLayout user={user}>
      {/* Estatísticas Iniciais */}
      <div className="grid grid-cols-3 gap-6">
        <InfoCard title="Roteadores" value="0" />
        <InfoCard title="DHCP Configurados" value="0" />
        <InfoCard title="VLANs Criadas" value="0" />
      </div>
      <button
  onClick={() => navigate("/detect-router")}
  className="mt-6 w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 rounded-lg"
>
  Configurar Roteador
</button>
    </DashboardLayout>
  );
}

function InfoCard({ title, value }) {
  return (
    <div className="bg-white shadow-lg rounded-xl p-6 text-center">
      <h3 className="text-lg font-semibold text-gray-700">{title}</h3>
      <p className="text-4xl font-bold text-blue-600 mt-2">{value}</p>
    </div>
  );
}



