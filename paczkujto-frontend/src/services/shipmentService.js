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

export const updateShipmentStatus = async (shipmentId, newStatus) => {
  return axios.put(
    `http://localhost:8000/shipments/update_status`,
    null,
    {
      params: {
        shipment_id: shipmentId,
        new_status: newStatus
      },
      headers: {
        Authorization: `Bearer ${getToken()}`
      }
    }
  );
};

export const assignCourierToShipment = async (shipmentId, courierId) => {
  return axios.put(
    `http://localhost:8000/shipments/assign`,
    null,
    {
      params: {
        shipment_id: shipmentId,
        courier_id: courierId
      },
      headers: {
        Authorization: `Bearer ${getToken()}`
      }
    }
  );
};