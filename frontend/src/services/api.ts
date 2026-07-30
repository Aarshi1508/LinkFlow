import axios from "axios";

// Single source of truth for talking to the backend. Components never
// import axios directly - they go through the resource-specific service
// files (authService, urlService), which all use this instance.
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

// Attach the JWT to every outgoing request, if we have one. Reading from
// localStorage here (rather than passing the token around as a prop/arg)
// keeps every service function's signature simple.
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("linkflow_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// If the backend ever says "your token is invalid/expired," clear it and
// send the user back to login rather than showing a confusing error state.
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("linkflow_token");
      if (window.location.pathname !== "/login") {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default api;
