import React from "react";
import { format } from "date-fns";
import { useNavigate } from "react-router-dom";
import RegistrarSalidaButton from "./RegistrarSalidaButton"; // Importa el componente

function RegistroDetalle({ registro }) {
  const navigate = useNavigate();

  console.log("Renderizando RegistroDetalle con registro:", registro); // Ayuda a verificar duplicados

  if (!registro) {
    return <p>Cargando detalles del registro...</p>; // O un componente de carga más visual
  }

  const formatearFecha = (fecha) => {
    return fecha ? format(new Date(fecha), "dd/MM/yyyy, hh:mm a") : "Pendiente";
  };

  const formatearCobro = (cobro) => {
    return cobro !== null ? `$${cobro.toFixed(2)}` : "Pendiente";
  };

  const handleSalidaRegistrada = () => {
    alert("Salida registrada exitosamente.");
    navigate("/registro-parqueo"); // Redirige a la página principal de registros
  };

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Detalles del Registro</h2>
      <div className="bg-white p-4 rounded-lg shadow">
        <p><strong>ID:</strong> {registro.id}</p>
        <p><strong>Placa:</strong> {registro.vehiculo.placa}</p>
        <p><strong>Tipo de Vehículo:</strong> {registro.vehiculo.tipo}</p>
        <p><strong>Fecha de Entrada:</strong> {formatearFecha(registro.fecha_entrada)}</p>
        <p><strong>Fecha de Salida:</strong> {formatearFecha(registro.fecha_salida)}</p>
        <p><strong>Tiempo Estacionado (minutos):</strong> {registro.tiempo_estacionado || "Pendiente"}</p>
        <p><strong>Total Cobro:</strong> {formatearCobro(registro.total_cobro)}</p>
        <p><strong>Estado:</strong> {registro.estado}</p>
      </div>
    </div>
  );
}

export default RegistroDetalle;
