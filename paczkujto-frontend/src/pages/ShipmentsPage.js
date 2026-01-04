import React, { useState, useEffect } from "react";
import { getAllShipments } from "../services/shipmentService";
import ShipmentCard from "../components/ShipmentCard";
import ShipmentDetailsModal from "../components/ShipmentDetailsModal";
import "../styles/ShipmentsPage.css";
import { translate } from "../i18n";

export default function ShipmentsPage() {
  const [shipments, setShipments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filterRole, setFilterRole] = useState("sender");
  const [selectedShipment, setSelectedShipment] = useState(null);

  useEffect(() => {
    fetchShipments();
  }, []);

  const fetchShipments = async () => {
    setLoading(true);
    try {
      const res = await getAllShipments();
      setShipments(res.data);
    } catch (error) {
      setError("Nie udało się pobrać przesyłek");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleViewDetails = (shipment) => {
    setSelectedShipment(shipment);
  };

  const closeModal = () => {
    setSelectedShipment(null);
  };

  const getFilteredShipments = () => {
    if (!shipments) return [];
    
    const userId = JSON.parse(localStorage.getItem("user"))?.id;
    const userEmail = JSON.parse(localStorage.getItem("user"))?.email;
    if (!userId) return shipments;
    
    switch (filterRole) {
      case "sender":
        return shipments.filter(s => s.sender_id === userId);
      case "recipient":
        return shipments.filter(s => s.recipient_email === userEmail);
      case "all":
      default:
        return shipments;
    }
  };

  const filteredShipments = getFilteredShipments();

  return (
    <div className="shipments-page">
      <h1>Moje przesyłki</h1>
      
      <div className="role-toggle" role="tablist" aria-label={translate("Filter by role")}>
        <button
          type="button"
          className={`role-toggle-btn${filterRole === "sender" ? " active" : ""}`}
          onClick={() => setFilterRole("sender")}
          aria-pressed={filterRole === "sender"}
        >
          {translate("Shipments I Sent")}
        </button>
        <button
          type="button"
          className={`role-toggle-btn${filterRole === "recipient" ? " active" : ""}`}
          onClick={() => setFilterRole("recipient")}
          aria-pressed={filterRole === "recipient"}
        >
          {translate("Shipments I Receive")}
        </button>
      </div>
      
      {loading ? (
        <div className="loading-indicator">Ładowanie przesyłek...</div>
      ) : error ? (
        <div className="error-message">{error}</div>
      ) : filteredShipments.length === 0 ? (
        <div className="no-shipments-message">
          {`Nie masz żadnych przesyłek jako ${filterRole === "sender" ? "nadawca" : "odbiorca"}`}
        </div>
      ) : (
        <div className="shipments-grid">
          {filteredShipments.map(shipment => (
            <ShipmentCard
              key={shipment.id}
              shipment={shipment}
              onDetails={() => handleViewDetails(shipment)}
            />
          ))}
        </div>
      )}
      
      {selectedShipment && (
        <ShipmentDetailsModal 
          shipment={selectedShipment} 
          onClose={closeModal} 
        />
      )}
    </div>
  );
}