import axios from "axios";

export const createPackage = async (packageData, shipment_id, token) => {
  return axios.post(
    `http://localhost:8000/packages?shipment_id=${shipment_id}`,
    packageData,
    { headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` } }
  );
};


export const getPackageByShipmentId = async (shipmentId) => {
  return axios.get(`http://localhost:8000/packages/${shipmentId}`);
};