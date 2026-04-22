import axios from "axios";

const apiBaseUrl =
  import.meta.env.VITE_API_URL ||
  `${window.location.protocol}//${window.location.hostname}:8000`;

export const api = axios.create({
  baseURL: apiBaseUrl,
  withCredentials: true,
});
