//Mostrará la lista de clientes y permitirá agregar, editar y eliminar clientes.

import { useEffect, useState } from "react";
import axios from 'axios';

function Clientes() {
  const [clientes, setClientes] = useState['clientes'];

  useEffect(() => {
    const fetchClientes = async () => {
      const response = await axios.get('/api/clientes/', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      setClientes(response.data);
    };
    fetchClientes();
  }, []);

  return (
    <div>
      <h2>Clientes</h2>
      <ul>
        {clientes.map(cliente => (
          <li key={cliente.id}>{cliente.nombre}</li>
        ))}
      </ul>
    </div>
  );
}

export default Clientes;