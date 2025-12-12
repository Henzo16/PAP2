import { useNavigate } from "react-router-dom";

export default function DashboardLayout({ children, user }) {
  const navigate = useNavigate();

  function logout() {
    localStorage.removeItem("token");
    navigate("/login");
  }

  return (
    <div className="flex h-screen bg-gray-100">
      {/* SIDEBAR */}
      <aside className="w-64 bg-white shadow-xl flex flex-col">
        <div className="p-6 border-b">
          <h2 className="text-xl font-bold text-blue-600">Cisco Manager</h2>
        </div>

        <nav className="flex-1 p-4 space-y-2">
          <MenuLink label="Dashboard" to="/dashboard" />
          <MenuLink label="Roteadores" to="/routers" />
          <MenuLink label="DHCP" to="/dhcp" />
          <MenuLink label="VLANs" to="/vlans" />
          <MenuLink label="NAT" to="/nat" />
          <MenuLink label="ACL" to="/acl" />
          <MenuLink label="OSPF" to="/ospf" />
          <MenuLink label="Logs" to="/logs" />
        </nav>

        <button
          onClick={logout}
          className="m-4 p-3 bg-red-500 hover:bg-red-600 text-white rounded-lg"
        >
          Logout
        </button>
      </aside>

      {/* CONTEÚDO PRINCIPAL */}
      <main className="flex-1 p-8 overflow-y-auto">
        {/* TOPBAR */}
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-800">Bem-vindo 👋</h1>

          <div className="text-right">
            <p className="font-semibold text-gray-700">{user?.nome}</p>
            <p className="text-sm text-gray-500">{user?.email}</p>
          </div>
        </div>

        {/* CONTEÚDO */}
        {children}
      </main>
    </div>
  );
}

function MenuLink({ label, to }) {
  return (
    <a
      href={to}
      className="block px-4 py-2 rounded-lg hover:bg-blue-100 text-gray-700 font-medium"
    >
      {label}
    </a>
  );
}
