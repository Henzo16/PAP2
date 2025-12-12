import { useState } from "react";
import { API_URL } from "../config";

export default function Register() {
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [confirmar, setConfirmar] = useState("");
  const [erro, setErro] = useState("");
  const [sucesso, setSucesso] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();
    setErro("");
    setSucesso("");

    if (senha !== confirmar) {
      setErro("As senhas não correspondem.");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nome, email, senha }),
      });

      const data = await response.json();

      if (!response.ok) {
        setErro(data.detail || "Erro ao registrar.");
        return;
      }

      setSucesso("Conta criada com sucesso! Pode fazer login.");
    } catch (err) {
      setErro("Não foi possível conectar ao servidor.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 bg-gray-100">
      <div className="w-full max-w-md bg-white shadow-xl rounded-2xl p-8 fade-in">
        <h1 className="text-3xl font-semibold text-center text-blue-600 mb-6">
          Criar Conta 
        </h1>

        {erro && <p className="text-red-600 font-medium">{erro}</p>}
        {sucesso && <p className="text-green-600 font-medium">{sucesso}</p>}

        <form className="space-y-5" onSubmit={handleRegister}>
          <div>
            <label className="block mb-1 font-medium">Nome completo</label>
            <input
              value={nome}
              onChange={(e) => setNome(e.target.value)}
              type="text"
              required
              className="w-full p-3 border rounded-lg"
            />
          </div>

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

          <div>
            <label className="block mb-1 font-medium">Confirmar senha</label>
            <input
              value={confirmar}
              onChange={(e) => setConfirmar(e.target.value)}
              type="password"
              required
              className="w-full p-3 border rounded-lg"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg font-medium transition"
          >
            Criar Conta
          </button>
        </form>

        <p className="text-center mt-4 text-gray-600">
          Já tem conta?{" "}
          <a href="/login" className="text-blue-600 hover:underline">
            Entrar
          </a>
        </p>
      </div>
    </div>
  );
}
