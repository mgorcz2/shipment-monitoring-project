import React, { useEffect, useState } from "react";
import { getAllShipments } from "../services/shipmentService";
import ShipmentCard from "../components/ShipmentCard";

export default function ShipmentsPage() {
  const [shipments, setShipments] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchShipments = async () => {
      setError("");
      try {
        const res = await getAllShipments();
        setShipments(res.data);
      } catch (err) {
        if (err.response && err.response.data && err.response.data.detail) {
          setError(err.response.data.detail);
        } else if (err.response) {
          setError("Błąd: " + err.response.status);
        } else {
          setError("Brak połączenia z serwerem");
        }
      }
    };
    fetchShipments();
  }, []);

  const handleDetails = (shipment) => {
    alert("Szczegóły przesyłki: " + JSON.stringify(shipment, null, 2));
    // Możesz tu przekierować do strony szczegółów przesyłki
  };

  return (
    <div style={{
      display: "flex",
      flexWrap: "wrap",
      justifyContent: "flex-start",
      gap: "16px",
      padding: "32px"
    }}>
      {error && <div style={{ color: "red", width: "100%" }}>{error}</div>}
      {shipments.map(shipment => (
        <ShipmentCard
          key={shipment.id}
          shipment={shipment}
          onDetails={handleDetails}
        />
      ))}
      {shipments.length === 0 && !error && (
        <div style={{ color: "#888" }}>Brak przesyłek do wyświetlenia.</div>
      )}
    </div>
  );
}