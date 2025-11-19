import axios from "axios";
import { getToken } from "./authService";


export const getUserByEmail = async (email) => {
  return axios.get(
    `http://localhost:8000/users/email/${email}`,{
    headers: {
      Authorization: `Bearer ${getToken()}`
    }});
};

export const getMyProfile = async () => {
  return axios.get(
    `http://localhost:8000/users/me`,{
      headers: {
        Authorization: `Bearer ${getToken()}`
      }
    });
};

export const registerUser = async (data) => {
  return axios.post(
    "http://localhost:8000/users/register",
    data,
    { headers: { "Content-Type": "application/json" } }
  );
};


export const getAllUsers = async (token) => {
  return await axios.get("http://localhost:8000/users/all",{
    headers: {
      Authorization: `Bearer ${getToken()}`
    }});
};


export const deleteUser = async (email) => {
  return axios.delete(
    `http://localhost:8000/users/delete/${email}`,{
      headers: {
        Authorization: `Bearer ${getToken()}`
      }
    });
};

export const getUsersByRole = async (role) => {
  return axios.get(
    `http://localhost:8000/users/role/${role}`,{
      headers: {
        Authorization: `Bearer ${getToken()}`
      }
    });
};

export const deleteMyAccount = async () => {
  return axios.delete(
    `http://localhost:8000/users/me`,{
      headers: {
        Authorization: `Bearer ${getToken()}`
      }
    });
};