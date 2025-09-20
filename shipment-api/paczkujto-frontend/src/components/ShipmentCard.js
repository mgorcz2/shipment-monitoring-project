import React from "react";
import "../styles/ShipmentCard.css";
import { translate } from "../i18n";
import { FaBox, FaTruck, FaCheckCircle, FaTimesCircle, 
         FaUndoAlt, FaQuestionCircle, FaExclamationTriangle } from "react-icons/fa";

export default function ShipmentCard({ shipment, onDetails }) {
  const getStatusIcon = (status) => {
  switch(status?.toLowerCase()) {
    case "ready_for_pickup": return <FaBox className="status-icon" />;
    case "out_for_delivery": return <FaTruck className="status-icon" />;
    case "delivered": return <FaCheckCircle className="status-icon" />;
    case "failed_attempt": return <FaTimesCircle className="status-icon" />;
    case "returned_to_sender": return <FaUndoAlt className="status-icon" />;
    case "lost": return <FaQuestionCircle className="status-icon" />;
    case "damaged": return <FaExclamationTriangle className="status-icon" />;
    default: return null;
  }
  };
  return (
    <div className="shipment-card">
      <span className={`shipment-status-badge status-${shipment.status?.toLowerCase()}`}>
        {getStatusIcon(shipment.status)}
        {translate(shipment.status)}
      </span>
      
      <div className="shipment-header">
        <span className="shipment-id">#{shipment.id}</span>
      </div>
      <div className="shipment-info">
        <div><strong>Nadawca:</strong> {shipment.sender_fullname|| "Nieznany"}</div>
        <div><strong>Odbiorca:</strong> {shipment.recipient_fullname || shipment.recipient_email || "Nieznany"}</div>
        <div><strong>Adres nadania:</strong> {shipment.origin}</div>
        <div><strong>Adres odbioru:</strong> {shipment.destination}</div>
      </div>
      <div className="shipment-actions">
        <button onClick={() => onDetails(shipment)}>Szczegóły</button>
      </div>
    </div>
  );
}