import axios from "axios";

import { getToken } from "./authService";
export const getAllStaff = async () => {
  return await axios.get("http://localhost:8000/staff/",
    { headers: { "Content-Type": "application/json" } }
  );
};

export const getStaffById = async (staffId) => {
  return await axios.get(
    `http://localhost:8000/staff/${staffId}`,
    { headers: { "Content-Type": "application/json" } }
  );
}