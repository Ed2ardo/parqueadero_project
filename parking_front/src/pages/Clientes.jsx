// Mostrará la lista de clientes y permitirá agregar, editar y eliminar clientes.
import { useEffect, useState } from "react";
import axios from 'axios';

function Clientes() {
  const [clientes, setClientes] = useState([]);
  const [error, setError] = useState(null);

  // Campos para agregar un nuevo cliente
  const [nombre, setNombre] = useState('');
  const [docIdentidad, setDocIdentidad] = useState('');
  const [email, setEmail] = useState('');
  const [telefono, setTelefono] = useState('');
  const [direccion, setDireccion] = useState('');

  // Estado para manejar la edición de cliente
  const [editandoCliente, setEditandoCliente] = useState(null);
  const [nuevoNombre, setNuevoNombre] = useState('');
  const [nuevoDocIdentidad, setNuevoDocIdentidad] = useState('');
  const [nuevoEmail, setNuevoEmail] = useState('');
  const [nuevoTelefono, setNuevoTelefono] = useState('');
  const [nuevoDireccion, setNuevoDireccion] = useState('');

  // Obtener la lista de clientes
  useEffect(() => {
    fetchClientes();
  }, []);

  const fetchClientes = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/clientes/');
      setClientes(response.data);
    } catch (error) {
      console.error("Error al obtener clientes:", error);
      setError("Error al obtener clientes");
    }
  };

  // Crear un nuevo cliente
  const handleAddCliente = async () => {
    try {
      const response = await axios.post('http://localhost:8000/api/clientes/', {
        nombre,
        doc_identidad: docIdentidad,
        email,
        telefono,
        direccion
      });
      setClientes([...clientes, response.data]);  // Agregar el nuevo cliente a la lista
      setNombre('');
      setDocIdentidad('');
      setEmail('');
      setTelefono('');
      setDireccion('');
    } catch (error) {
      console.error("Error al agregar cliente:", error);
      setError("Error al agregar cliente");
    }
  };

  // Iniciar edición de cliente
  const iniciarEdicion = (cliente) => {
    setEditandoCliente(cliente.id);
    setNuevoNombre(cliente.nombre);
    setNuevoDocIdentidad(cliente.doc_identidad);
    setNuevoEmail(cliente.email || '');
    setNuevoTelefono(cliente.telefono || '');
    setNuevoDireccion(cliente.direccion || '');
  };

  // Guardar edición de cliente
  const handleEditCliente = async () => {
    try {
      const response = await axios.put(`http://localhost:8000/api/clientes/${editandoCliente}/`, {
        nombre: nuevoNombre,
        doc_identidad: nuevoDocIdentidad,
        email: nuevoEmail,
        telefono: nuevoTelefono,
        direccion: nuevoDireccion
      });
      const updatedClientes = clientes.map(cliente =>
        cliente.id === editandoCliente ? response.data : cliente
      );
      setClientes(updatedClientes);
      setEditandoCliente(null);
      setNuevoNombre('');
      setNuevoDocIdentidad('');
      setNuevoEmail('');
      setNuevoTelefono('');
      setNuevoDireccion('');
    } catch (error) {
      console.error("Error al editar cliente:", error);
      setError("Error al editar cliente");
    }
  };

  // Eliminar cliente
  const handleDeleteCliente = async (id) => {
    try {
      await axios.delete(`http://localhost:8000/api/clientes/${id}/`);
      setClientes(clientes.filter(cliente => cliente.id !== id));
    } catch (error) {
      console.error("Error al eliminar cliente:", error);
      setError("Error al eliminar cliente");
    }
  };

  return (
    <div>
      <h2>Clientes</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {/* Lista de Clientes */}
      <ul>
        {Array.isArray(clientes) ? (
          clientes.map(cliente => (
            <li key={cliente.id}>
              {editandoCliente === cliente.id ? (
                <>
                  <input
                    type="text"
                    value={nuevoNombre}
                    onChange={(e) => setNuevoNombre(e.target.value)}
                    placeholder="Nombre"
                  />
                  <input
                    type="text"
                    value={nuevoDocIdentidad}
                    onChange={(e) => setNuevoDocIdentidad(e.target.value)}
                    placeholder="Documento de Identidad"
                  />
                  <input
                    type="email"
                    value={nuevoEmail}
                    onChange={(e) => setNuevoEmail(e.target.value)}
                    placeholder="Email"
                  />
                  <input
                    type="text"
                    value={nuevoTelefono}
                    onChange={(e) => setNuevoTelefono(e.target.value)}
                    placeholder="Teléfono"
                  />
                  <input
                    type="text"
                    value={nuevoDireccion}
                    onChange={(e) => setNuevoDireccion(e.target.value)}
                    placeholder="Dirección"
                  />
                  <button onClick={handleEditCliente}>Guardar</button>
                  <button onClick={() => setEditandoCliente(null)}>Cancelar</button>
                </>
              ) : (
                <>
                  {cliente.nombre} - {cliente.doc_identidad}
                  <button onClick={() => iniciarEdicion(cliente)}>Editar</button>
                  <button onClick={() => handleDeleteCliente(cliente.id)}>Eliminar</button>
                </>
              )}
            </li>
          ))
        ) : (
          <p>No hay clientes disponibles para mostrar.</p>
        )}
      </ul>

      {/* Formulario para Agregar Cliente */}
      <div>
        <h3>Agregar Cliente</h3>
        <input
          type="text"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
          placeholder="Nombre"
        />
        <input
          type="text"
          value={docIdentidad}
          onChange={(e) => setDocIdentidad(e.target.value)}
          placeholder="Documento de Identidad"
        />
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
        />
        <input
          type="text"
          value={telefono}
          onChange={(e) => setTelefono(e.target.value)}
          placeholder="Teléfono"
        />
        <input
          type="text"
          value={direccion}
          onChange={(e) => setDireccion(e.target.value)}
          placeholder="Dirección"
        />
        <button onClick={handleAddCliente}>Agregar</button>
      </div>
    </div>
  );
}

export default Clientes;
