import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import { useContext } from "react";
import { AuthContext } from "./context/AuthContext";
import RouterSetup from "./pages/RouterSetup";
import DetectRouterPage from "./pages/DetectRouterPage";
import ServiceConfigPage from "./pages/ServiceConfigPage";
import DhcpPage from "./services/DhcpPage";




export default function App() {
  const { user, loading } = useContext(AuthContext);

  if (loading) {
    return <p className="text-center mt-10">Carregando...</p>;
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={user ? <Navigate to="/dashboard" /> : <Navigate to="/login" />}
        />
        
        <Route
          path="/login"
          element={!user ? <Login /> : <Navigate to="/dashboard" />}
        />

        <Route
          path="/register"
          element={!user ? <Register /> : <Navigate to="/dashboard" />}
        />

        <Route
          path="/dashboard"
          element={user ? <Dashboard /> : <Navigate to="/login" />}
        />
        <Route path="/router-setup" element={<RouterSetup />} />
        <Route path="/detect-router" element={<DetectRouterPage />} />
        <Route path="/services" element={<ServiceConfigPage />} />
        <Route path="/services/dhcp" element={<DhcpPage />} />

      </Routes>
    </BrowserRouter>
  );
}


 







