import axios from "axios";

export const registerUser = async (data) => {
  return axios.post(
    "http://localhost:8000/users/register",
    data,
    { headers: { "Content-Type": "application/json" } }
  );
};