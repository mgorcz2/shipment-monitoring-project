import axios from "axios";

import { getToken } from "./authService";
export const getAllStaff = async () => {
  return await axios.get("http://localhost:8000/staff/",
    { headers: { "Content-Type": "application/json" } }
  );
};

export const getStaffById = async (staffId) => {
  const token = getToken();
  return await axios.get(
    `http://localhost:8000/staff/${staffId}`,
    { headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` } }
  );
}

export const registerStaff = async (userData, staffData) => {
  const token = getToken();
  return await axios.post(
    `http://localhost:8000/staff/register`,
    { user_data: userData, staff: staffData },
    { headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` } }
  );
};
