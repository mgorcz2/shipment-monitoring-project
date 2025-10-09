import axios from "axios";
import { jwtDecode } from "jwt-decode";
import { Navigate, Outlet } from "react-router-dom";

export const login = async (email, password) => {
  const params = new URLSearchParams();
  params.append("username", email);
  params.append("password", password);

  return axios.post("http://localhost:8000/users/token", params, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" }
  });
};

export const getToken = () => localStorage.getItem("token");

export const isTokenValid = () => {
  const token = getToken();
  if (!token) return false;
  try {
    const { exp } = jwtDecode(token);
    if (!exp) return false;
    return Date.now() < exp * 1000;
  } catch {
    return false;
  }
};

export const isLoggedIn = () => isTokenValid();


export const logout = () => {
  localStorage.clear();
  window.location.href = "/login";
};


export const getUserRole = () => {
  try {
    const userDataString = localStorage.getItem("user");
    if (!userDataString) return null;
    
    const UserData = JSON.parse(userDataString);
    return UserData.role || null;
  } catch {
    return null;
  }
};
const ProtectedRoute = ({ allowedRoles = [] }) => {
  const isAuthenticated = isTokenValid();
  
  const userRole = getUserRole();
  
  if (!isAuthenticated || !userRole || !allowedRoles.includes(userRole)) {
    return <Navigate to="/" replace />;
  }
  
  return <Outlet />;
};

export default ProtectedRoute;