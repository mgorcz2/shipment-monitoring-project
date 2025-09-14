import axios from "axios";
import { getToken } from "./authService";

export const getAllShipments = async () => {
  return axios.get("http://localhost:8000/shipments/all", {
    headers: {
      Authorization: `Bearer ${getToken()}`
    }
  });
};