import axios from "axios";

axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (
      error.response?.status === 401 ||
      (error.response?.status === 500 && 
       error.response?.data?.detail?.includes("No user found"))
    ) {
      localStorage.clear();
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default axios;
