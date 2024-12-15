import axios from "axios";

const axiosInstance = axios.create({
  baseURL: "http://127.0.0.1:8000/api/", // Ajusta según la URL de tu backend
  timeout: 5000,
});

export default axiosInstance;
