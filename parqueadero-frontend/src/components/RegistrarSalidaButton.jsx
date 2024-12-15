import React from "react";
import axios from "../services/axiosInstance";

function RegistrarSalidaButton({ registroId, onSalidaRegistrada }) {
  const handleRegistrarSalida = async () => {
    try {
      await axios.post(`/gestion_parqueadero/registros/${registroId}/registrar_salida/`);
      alert("Salida registrada exitosamente.");
      onSalidaRegistrada(registroId);
    } catch (error) {
      console.error("Error al registrar salida:", error.response?.data || error.message);
      alert("No se pudo registrar la salida. Inténtalo de nuevo.");
    }
  };

  return (
    <button
      onClick={handleRegistrarSalida}
      className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
    >
      Registrar Salida
    </button>
  );
}

export default RegistrarSalidaButton;
