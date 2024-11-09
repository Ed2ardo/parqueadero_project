// llamadas al backend
import axios from "axios";

const api = axios.create({
  baseURL: "/api",
  headers: {
    "Content-Type": "application/json",
  },
});

export const login = (credentials) => api.post("/auth/login/", credentials);
export const getClientes = () => api.get("/clientes/");
// añadir las funciones para facturas, parqueo, etc.

export default api;
