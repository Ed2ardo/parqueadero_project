import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom'; // Importa useNavigate
import axios from "../services/axiosInstance";
import RegistroDetalle from '../components/RegistroDetalle';
import Layout from "../components/Layout";
import RegistrarSalidaButton from '../components/RegistrarSalidaButton';

function RegistroDetallePage() {
  const { id } = useParams(); // Obtiene el ID de la URL
  const navigate = useNavigate(); // Hook para redireccionar
  const [registro, setRegistro] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRegistro = async () => {
      try {
        const response = await axios.get(`/gestion_parqueadero/registros/${id}/`); // Petición con el ID
        setRegistro(response.data);
      } catch (err) {
        setError("Error al cargar el registro.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchRegistro();
  }, [id]); // El useEffect depende del ID

  if (loading) {
    return <p>Cargando...</p>; // Muestra un mensaje de carga
  }

  if (error) {
    return <p className="text-red-500">{error}</p>; // Muestra el mensaje de error
  }

  return (
    <Layout>
      <RegistroDetalle registro={registro} />
      {registro && !registro.fecha_salida && (
        <RegistrarSalidaButton
          registroId={registro.id}
          onSalidaRegistrada={() => {
            // Actualiza el estado local y redirige al listado de registros
            setRegistro({ ...registro, fecha_salida: new Date() });
            navigate("/registro-parqueo"); // Redirige a la página principal
          }}
        />
      )}
    </Layout>
  );
}

export default RegistroDetallePage;
