import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api"; // Importa la configuración de Axios

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Verifica si ya hay un token en localStorage y redirige a /clientes si existe
    const token = localStorage.getItem("token");
    if (token) {
      navigate("/clientes");
    }
  }, [navigate]);

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      // Envia las credenciales para el inicio de sesión
      const response = await api.post("http://localhost:8000/api/auth/login/", { username, password });

      // Guarda el token en localStorage y redirige a /clientes
      localStorage.setItem("token", response.data.token);
      navigate("/clientes");
    } catch (error) {
      // Manejo de errores en caso de credenciales inválidas o problemas con la red
      setError("Credenciales incorrectas o error en la conexión");
      console.error("Error al iniciar sesión:", error);
    }
  };

  return (
    <div>
      <h2>Iniciar Sesión</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleLogin}>
        <div>
          <label>Usuario:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Contraseña:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Iniciar Sesión</button>
      </form>
    </div>
  );
}

export default Login;
