// Aquí se autenticarán los usuarios, y si la autenticación es correcta, se almacenará el token para futuras solicitudes.

import { useState } from 'react';
import { Form, useNavigate } from 'react-router-dom';
import axios from 'axios';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/auth/login/', { username, password })
      localStorage.setItem('token', response.data.token);
      navigate('/clientes')
    } catch (error) {
      console.error("Error al iniciar sesión", error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" placeholder='Usuario' value={username} onChange={(e) => setUsername(e.target.value)} />
      <input type="password" placeholder='Contraseña' value={password} onChange={(e) => setPassword(e.target.value)} />
      <button type="submit">Iniciar sesión</button>
    </form>
  );

}

export default Login;