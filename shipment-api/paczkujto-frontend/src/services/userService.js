import axios from "axios";

export const getUserByEmail = async (email, token) => {
  return axios.get(
    `http://localhost:8000/users/email/${email}`,
    { headers: { Authorization: `Bearer ${token}` } }
  );
};

export const registerUser = async (data) => {
  return axios.post(
    "http://localhost:8000/users/register",
    data,
    { headers: { "Content-Type": "application/json" } }
  );
};