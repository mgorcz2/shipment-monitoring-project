import axios from "axios";
import { getToken } from "./authService";


export const createPackageWithShipment = async (packageData, shipmentData) => {
  return axios.post(
    `http://localhost:8000/packages/add`,
    {
      package: packageData,
      shipment_data: shipmentData
    },
    {
      headers: {
      Authorization: `Bearer ${getToken()}`
    }});
};


export const getPackageByShipmentId = async (shipmentId) => {
  return axios.get(`http://localhost:8000/packages/${shipmentId}`, {
      headers: {
      Authorization: `Bearer ${getToken()}`
    }});
};

