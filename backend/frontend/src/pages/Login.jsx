import { useState, useContext } from "react";
import { API_URL } from "../config";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

export default function Login() {
  const navigate = useNavigate();
  const { setUser } = useContext(AuthContext);

  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setErro("");

    try {
      // 1️⃣ Login → recebe o token
      const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, senha }),
      });

      const data = await response.json();

      // 2️⃣ Erro no login
      if (!response.ok) {
        return setErro(data.detail || "Email ou senha incorretos.");
      }

      // 3️⃣ Guardar token
      localStorage.setItem("token", data.access_token);

      // 4️⃣ Obter dados do usuário autenticado
      const meRes = await fetch(`${API_URL}/auth/me`, {
        headers: { Authorization: `Bearer ${data.access_token}` },
      });

      const userData = await meRes.json();

      if (!meRes.ok) {
        setErro("Erro ao carregar dados do usuário.");
        return;
      }

      // 5️⃣ Atualizar contexto global
      setUser(userData);

      // 6️⃣ Redirecionar
      navigate("/dashboard");
    } catch (err) {
      console.error(err);
      setErro("Erro ao conectar ao servidor.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 bg-gray-100">
      <div className="w-full max-w-md bg-white shadow-xl rounded-2xl p-8 fade-in">
        <h1 className="text-3xl font-semibold text-center text-blue-600 mb-6">
          LOGIN
        </h1>

        {erro && <p className="text-red-600 font-medium">{erro}</p>}

        <form className="space-y-5" onSubmit={handleLogin}>
          <div>
            <label className="block mb-1 font-medium">Email</label>
            <input
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              type="email"
              required
              className="w-full p-3 border rounded-lg"
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">Senha</label>
            <input
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              type="password"
              required
              className="w-full p-3 border rounded-lg"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg font-medium transition"
          >
            Entrar
          </button>
        </form>

        <p className="text-center mt-4 text-gray-600">
          Ainda não tem conta?{" "}
          <a href="/register" className="text-blue-600 hover:underline">
            Criar conta
          </a>
        </p>
      </div>
    </div>
  );
}
