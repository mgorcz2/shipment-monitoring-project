import axios from "axios";

export const registerClient = async (data, user_id) => {
  return axios.post(
    `http://localhost:8000/client/register?user_id=${user_id}`,
    data,
    { headers: { "Content-Type": "application/json" } }
  );
};


export const getClientById = async (userId, token) => {
  return axios.get(
    `http://localhost:8000/client/${userId}`,
    { headers: { Authorization: `Bearer ${token}` } }
  );
};
