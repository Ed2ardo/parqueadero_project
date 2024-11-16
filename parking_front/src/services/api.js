// llamadas al backend
import axios from "axios";

const token = localStorage.getItem("token");

const api = axios.create({
  baseURL: "http://localhost:8000/api",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${localStorage.getItem("token")}`, // Autorización global
  },
});

// Agrega el token a las solicitudes
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const login = (credentials) => api.post("/auth/login/", credentials);
export const getClientes = () => api.get("/clientes/");
export const getVehiculos = () => api.get("/gestion_parqueadero/vehiculos/");
// añadir las funciones para facturas, parqueo, etc.

export default api;
