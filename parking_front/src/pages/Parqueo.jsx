import { useEffect, useState } from "react";
import axios from 'axios';

function Parqueo() {
  const [espacios, setEspacios] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchEspacios();
  }, []);

  const fetchEspacios = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/espacios/');
      setEspacios(response.data);
    } catch (error) {
      console.error("Error al obtener espacios de parqueo:", error);
      setError("Error al obtener espacios de parqueo");
    }
  };

  const toggleEstado = async (id, ocupado) => {
    try {
      const response = await axios.patch(`http://localhost:8000/api/espacios/${id}/`, {
        ocupado: !ocupado
      });
      setEspacios(espacios.map(espacio =>
        espacio.id === id ? { ...espacio, ocupado: response.data.ocupado } : espacio
      ));
    } catch (error) {
      console.error("Error al cambiar estado:", error);
      setError("Error al cambiar estado del espacio");
    }
  };

  return (
    <div className="parqueo">
      <h2>Espacios de Parqueo</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <ul>
        {espacios.map(espacio => (
          <li key={espacio.id}>
            Espacio {espacio.numero} - {espacio.ocupado ? "Ocupado" : "Libre"}
            <button onClick={() => toggleEstado(espacio.id, espacio.ocupado)}>
              Cambiar estado
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Parqueo;
