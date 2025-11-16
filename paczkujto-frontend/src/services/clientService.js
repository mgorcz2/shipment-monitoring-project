import axios from "axios";
import { getToken } from "./authService";

export const registerClient = async (userData, clientData) => {
  return axios.post(
    `http://localhost:8000/client/register`,
    { user_data: userData, client: clientData },
    { headers: { "Content-Type": "application/json" } }
  );
};


export const getClientById = async (userId, token) => {
  return axios.get(
    `http://localhost:8000/client/${userId}`,
    { headers: {
          Authorization: `Bearer ${getToken()}`
        }});
};

