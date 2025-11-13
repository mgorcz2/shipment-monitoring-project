import React, { useState, useEffect } from "react";
import { getAllShipments } from "../services/shipmentService";
import ShipmentDetailsModal from "../components/ShipmentDetailsModal";
import { translate } from "../i18n";
import "../styles/ShipmentsPage.css";

export default function CourierShipmentsPage() {
  const [shipments, setShipments] = useState([]);
  const [filteredShipments, setFilteredShipments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedShipment, setSelectedShipment] = useState(null);
  const [filterStatus, setFilterStatus] = useState("all");
  const [sortBy, setSortBy] = useState("created_at");
  

  useEffect(() => {
    fetchShipments();
  }, []);

  useEffect(() => {
    applyFiltersAndSort();
  }, [shipments, filterStatus, sortBy]);

  const fetchShipments = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await getAllShipments();
      setShipments(response.data);
    } catch (err) {
      console.error("Błąd podczas pobierania przesyłek:", err);
      setError("Nie udało się pobrać listy przesyłek");
    } finally {
      setLoading(false);
    }
  };

  const applyFiltersAndSort = () => {
    let result = [...shipments];

    if (filterStatus !== "all") {
      result = result.filter(s => s.status === filterStatus);
    }
    result.sort((a, b) => {
      switch (sortBy) {
        case "created_at":
          return new Date(b.created_at) - new Date(a.created_at);
        case "status":
          return (a.status || "").localeCompare(b.status || "");
        case "destination":
          return (a.destination || "").localeCompare(b.destination || "");
        default:
          return 0;
      }
    });

    setFilteredShipments(result);
  };

  const handleStatusChange = async (shipmentId, newStatus) => {
    console.log(`Zmiana statusu przesyłki ${shipmentId} na ${newStatus}`);
  };

  const getStatusColor = (status) => {
    switch(status?.toLowerCase()) {
      case "ready_for_pickup": return "#FFA500";
      case "out_for_delivery": return "#1E90FF";
      case "delivered": return "#28a745";
      case "failed_attempt": return "#dc3545";
      case "returned_to_sender": return "#6c757d";
      default: return "#6c757d";
    }
  };

  if (loading) {
    return <div className="loading-container">Ładowanie przesyłek...</div>;
  }

  if (error) {
    return <div className="error-container">{error}</div>;
  }

  return (
    <div className="shipments-page">
      <div className="shipments-header">
        <h1>Moje dostawy</h1>
        <p>Zarządzaj przypisanymi przesyłkami</p>
      </div>

      <div className="shipments-controls">
        <div className="filter-section">
          <label htmlFor="filter-status">Filtruj po statusie:</label>
          <select
            id="filter-status"
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
          >
            <option value="all">Wszystkie</option>
            <option value="ready_for_pickup">Gotowe do odbioru</option>
            <option value="out_for_delivery">W trasie</option>
            <option value="delivered">Dostarczone</option>
            <option value="failed_attempt">Nieudana próba</option>
            <option value="returned_to_sender">Zwrócone</option>
          </select>
        </div>

        <div className="sort-section">
          <label htmlFor="sort-by">Sortuj według:</label>
          <select
            id="sort-by"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
          >
            <option value="created_at">Data utworzenia</option>
            <option value="status">Status</option>
            <option value="destination">Miejsce docelowe</option>
          </select>
        </div>

        <button className="refresh-btn" onClick={fetchShipments}>
          🔄 Odśwież
        </button>
      </div>

      <div className="shipments-stats">
        <div className="stat-card">
          <span className="stat-label">Wszystkie</span>
          <span className="stat-value">{shipments.length}</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Do odbioru</span>
          <span className="stat-value">
            {shipments.filter(s => s.status === "ready_for_pickup").length}
          </span>
        </div>
        <div className="stat-card">
          <span className="stat-label">W trasie</span>
          <span className="stat-value">
            {shipments.filter(s => s.status === "out_for_delivery").length}
          </span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Dostarczone</span>
          <span className="stat-value">
            {shipments.filter(s => s.status === "delivered").length}
          </span>
        </div>
      </div>

      {filteredShipments.length === 0 ? (
        <div className="no-shipments">
          <p>Brak przesyłek spełniających wybrane kryteria</p>
        </div>
      ) : (
        <div className="courier-shipments-table">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Status</th>
                <th>Odbiorca</th>
                <th>Adres nadania</th>
                <th>Adres docelowy</th>
                <th>Data utworzenia</th>
                <th>Akcje</th>
              </tr>
            </thead>
            <tbody>
              {filteredShipments.map((shipment) => (
                <tr key={shipment.id}>
                  <td>#{shipment.id}</td>
                  <td>
                    <span 
                      className="table-status-badge"
                      style={{ backgroundColor: getStatusColor(shipment.status) }}
                    >
                      {translate(shipment.status)}
                    </span>
                  </td>
                  <td>{shipment.recipient_fullname || shipment.recipient_email || "Nieznany"}</td>
                  <td>{shipment.origin}</td>
                  <td>{shipment.destination}</td>
                  <td>{new Date(shipment.created_at).toLocaleDateString()}</td>
                  <td>
                    <div className="table-actions">
                      <button
                        className="btn-details"
                        onClick={() => setSelectedShipment(shipment)}
                        title="Szczegóły"
                      >
                        📋
                      </button>
                      <button
                        className="btn-status"
                        onClick={() => {
                          console.log("Zmiana statusu", shipment.id);
                        }}
                        title="Zmień status"
                      >
                        🔄
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {selectedShipment && (
        <ShipmentDetailsModal
          shipment={selectedShipment}
          onClose={() => setSelectedShipment(null)}
        />
      )}
    </div>
  );
}