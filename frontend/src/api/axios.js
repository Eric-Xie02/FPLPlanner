import axios from "axios";

const axiosInstance = axios.create({
  baseURL: "", // will proxy to localhost:8000
  headers: {
    "Content-Type": "application/json",
  },
});

export default axiosInstance;
