import React, { useState, useEffect } from "react";
import { getAllShipments } from "../services/shipmentService";
import ShipmentCard from "../components/ShipmentCard";
import ShipmentDetailsModal from "../components/ShipmentDetailsModal"; // Dodaj ten import
import "../styles/ShipmentsPage.css";
import { translate } from "../i18n";

export default function ShipmentsPage() {
  const [shipments, setShipments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filterRole, setFilterRole] = useState("all");
  const [selectedShipment, setSelectedShipment] = useState(null); // Dodaj ten stan

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

  // Dodaj te dwie funkcje
  const handleViewDetails = (shipment) => {
    setSelectedShipment(shipment);
  };

  const closeModal = () => {
    setSelectedShipment(null);
  };

  // Filtrowanie przesyłek na podstawie wybranej roli
  const getFilteredShipments = () => {
    if (!shipments) return [];
    
    const userId = JSON.parse(localStorage.getItem("user"))?.id;
    if (!userId) return shipments;
    
    switch (filterRole) {
      case "sender":
        return shipments.filter(s => s.sender_id === userId);
      case "recipient":
        return shipments.filter(s => s.recipient_id === userId);
      case "all":
      default:
        return shipments;
    }
  };

  const filteredShipments = getFilteredShipments();

  return (
    <div className="shipments-page">
      <h1>Moje przesyłki</h1>
      
      <div className="filter-controls">
        <label htmlFor="role-filter">{translate("Filter by role")}:</label>
        <select 
          id="role-filter" 
          value={filterRole}
          onChange={(e) => setFilterRole(e.target.value)}
          className="role-filter-select"
        >
          <option value="all">{translate("All Shipments")}</option>
          <option value="sender">{translate("Shipments I Sent")}</option>
          <option value="recipient">{translate("Shipments I Receive")}</option>
        </select>
      </div>
      
      {loading ? (
        <div className="loading-indicator">Ładowanie przesyłek...</div>
      ) : error ? (
        <div className="error-message">{error}</div>
      ) : filteredShipments.length === 0 ? (
        <div className="no-shipments-message">
          {filterRole === "all" 
            ? "Nie masz jeszcze żadnych przesyłek" 
            : `Nie masz żadnych przesyłek jako ${filterRole === "sender" ? "nadawca" : "odbiorca"}`
          }
        </div>
      ) : (
        <div className="shipments-grid">
          {filteredShipments.map(shipment => (
            <ShipmentCard
              key={shipment.id}
              shipment={shipment}
              // Zmień tę linię
              onDetails={() => handleViewDetails(shipment)}
            />
          ))}
        </div>
      )}
      
      {/* Dodaj ten fragment */}
      {selectedShipment && (
        <ShipmentDetailsModal 
          shipment={selectedShipment} 
          onClose={closeModal} 
        />
      )}
    </div>
  );
}