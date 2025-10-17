import axios from "axios";
import { getToken } from "./authService";

export const getAllShipments = async () => {
  return axios.get("http://localhost:8000/shipments/all", {
    headers: {
      Authorization: `Bearer ${getToken()}`
    }
  });
};


export const createShipment = async (shipmentData, token) => {
  return axios.post(
    "http://localhost:8000/shipments/add",
    shipmentData,
    { headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` } }
  );
};