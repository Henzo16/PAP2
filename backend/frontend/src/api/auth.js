const API_URL = "http://127.0.0.1:8000/api/auth";

export async function login(email, senha) {
  const res = await fetch(`${API_URL}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, senha }),
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || "Erro desconhecido");
  }

  return res.json(); 
}

export async function register(nome, email, senha) {
  const res = await fetch(`${API_URL}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ nome, email, senha }),
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || "Erro no registro");
  }

  return res.json();
}
