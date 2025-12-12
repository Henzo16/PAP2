import { createContext, useState, useEffect } from "react";
import { API_URL } from "../config";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  async function loadUser() {
    const token = localStorage.getItem("token");

    // Nenhum token salvo → usuário deslogado
    if (!token) {
      setUser(null);
      setLoading(false);
      return;
    }

    try {
      const res = await fetch(`${API_URL}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      // Se a API retornar QUALQUER erro → deslogar o usuário
      if (!res.ok) {
        console.warn("Token inválido, removendo...");
        localStorage.removeItem("token");
        setUser(null);
      } else {
        const data = await res.json();
        setUser(data);
      }
    } catch (err) {
      console.error("Erro ao carregar usuário:", err);
      setUser(null);
      localStorage.removeItem("token");
    }

    setLoading(false);
  }

  useEffect(() => {
    loadUser();
  }, []);

  return (
    <AuthContext.Provider value={{ user, setUser, loading }}>
      {children}
    </AuthContext.Provider>
  );
}
