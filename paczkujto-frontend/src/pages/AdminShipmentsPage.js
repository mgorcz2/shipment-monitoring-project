import React, { useState, useEffect } from "react";
import { getAllShipments } from "../services/shipmentService";
import ShipmentDetailsModal from "../components/ShipmentDetailsModal";
import UpdatePackageStatusModal from "../components/UpdateShipmentStatusModal";
import AssignCourierModal from "../components/AssignCourierModal";
import { translate } from "../i18n";
import "../styles/ShipmentsPage.css";

export default function AdminShipmentsPage() {
  const [shipments, setShipments] = useState([]);
  const [filteredShipments, setFilteredShipments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedShipment, setSelectedShipment] = useState(null);
  const [statusModalShipment, setStatusModalShipment] = useState(null);
  const [courierModalShipment, setCourierModalShipment] = useState(null);
  
  // Filtry
  const [filterStatus, setFilterStatus] = useState("all");
  const [filterSender, setFilterSender] = useState("");
  const [filterRecipient, setFilterRecipient] = useState("");
  const [filterCourier, setFilterCourier] = useState("all");
  const [filterDateFrom, setFilterDateFrom] = useState("");
  const [filterDateTo, setFilterDateTo] = useState("");
  const [sortBy, setSortBy] = useState("created_at");
  

  useEffect(() => {
    fetchShipments();
  }, []);

  useEffect(() => {
    applyFiltersAndSort();
  }, [shipments, filterStatus, filterSender, filterRecipient, filterCourier, filterDateFrom, filterDateTo, sortBy]);

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

    if (filterSender.trim()) {
      result = result.filter(s => 
        s.sender_fullname?.toLowerCase().includes(filterSender.toLowerCase()) ||
        s.sender_email?.toLowerCase().includes(filterSender.toLowerCase())
      );
    }


    if (filterRecipient.trim()) {
      result = result.filter(s => 
        s.recipient_fullname?.toLowerCase().includes(filterRecipient.toLowerCase()) ||
        s.recipient_email?.toLowerCase().includes(filterRecipient.toLowerCase())
      );
    }

    if (filterCourier !== "all") {
      if (filterCourier === "assigned") {
        result = result.filter(s => s.courier_id !== null);
      } else if (filterCourier === "unassigned") {
        result = result.filter(s => s.courier_id === null);
      }
    }

    if (filterDateFrom) {
      const dateFrom = new Date(filterDateFrom);
      result = result.filter(s => new Date(s.created_at) >= dateFrom);
    }

    if (filterDateTo) {
      const dateTo = new Date(filterDateTo);
      dateTo.setHours(23, 59, 59, 999);
      result = result.filter(s => new Date(s.created_at) <= dateTo);
    }

    result.sort((a, b) => {
      switch (sortBy) {
        case "created_at":
          return new Date(b.created_at) - new Date(a.created_at);
        case "created_at_asc":
          return new Date(a.created_at) - new Date(b.created_at);
        case "status":
          return (a.status || "").localeCompare(b.status || "");
        case "destination":
          return (a.destination || "").localeCompare(b.destination || "");
        case "sender":
          return (a.sender_fullname || "").localeCompare(b.sender_fullname || "");
        case "recipient":
          return (a.recipient_fullname || "").localeCompare(b.recipient_fullname || "");
        default:
          return 0;
      }
    });

    setFilteredShipments(result);
  };

  const getStatusColor = (status) => {
    switch(status?.toLowerCase()) {
      case "pending": return "#808080";
      case "ready_for_pickup": return "#FFA500";
      case "picked_up": return "#FF8C00";
      case "out_for_delivery": return "#1E90FF";
      case "delivered": return "#28a745";
      case "failed_attempt": return "#dc3545";
      case "returned_to_sender": return "#6c757d";
      default: return "#6c757d";
    }
  };

  const clearFilters = () => {
    setFilterStatus("all");
    setFilterSender("");
    setFilterRecipient("");
    setFilterCourier("all");
    setFilterDateFrom("");
    setFilterDateTo("");
    setSortBy("created_at");
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
        <h1>Zarządzanie przesyłkami</h1>
        <p>Przeglądaj i zarządzaj wszystkimi przesyłkami w systemie</p>
      </div>

      <div className="shipments-stats">
        <div className="stat-card">
          <span className="stat-label">Wszystkie</span>
          <span className="stat-value">{shipments.length}</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Oczekujące</span>
          <span className="stat-value">
            {shipments.filter(s => s.status === "pending").length}
          </span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Gotowe do odbioru</span>
          <span className="stat-value">
            {shipments.filter(s => s.status === "ready_for_pickup").length}
          </span>
        </div>
        <div className="stat-card">
          <span className="stat-label">W trasie</span>
          <span className="stat-value">
            {shipments.filter(s => s.status === "out_for_delivery" || s.status === "picked_up").length}
          </span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Dostarczone</span>
          <span className="stat-value">
            {shipments.filter(s => s.status === "delivered").length}
          </span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Bez kuriera</span>
          <span className="stat-value">
            {shipments.filter(s => !s.courier_id).length}
          </span>
        </div>
      </div>

      <div className="admin-filters-panel">
        <div className="filters-row-fixed">
          <div className="filter-section">
            <label htmlFor="filter-status">Status:</label>
            <select
              id="filter-status"
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
            >
              <option value="all">Wszystkie</option>
              <option value="pending">Oczekujące</option>
              <option value="ready_for_pickup">Gotowe do odbioru</option>
              <option value="picked_up">Odebrane</option>
              <option value="out_for_delivery">W trasie</option>
              <option value="delivered">Dostarczone</option>
              <option value="failed_attempt">Nieudana próba</option>
              <option value="returned_to_sender">Zwrócone</option>
            </select>
          </div>

          <div className="filter-section">
            <label htmlFor="filter-courier">Kurier:</label>
            <select
              id="filter-courier"
              value={filterCourier}
              onChange={(e) => setFilterCourier(e.target.value)}
            >
              <option value="all">Wszyscy</option>
              <option value="assigned">Przypisani</option>
              <option value="unassigned">Bez przypisania</option>
            </select>
          </div>

          <div className="filter-section">
            <label htmlFor="sort-by">Sortuj według:</label>
            <select
              id="sort-by"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="created_at">Data utworzenia (najnowsze)</option>
              <option value="created_at_asc">Data utworzenia (najstarsze)</option>
              <option value="status">Status</option>
              <option value="destination">Miejsce docelowe</option>
              <option value="sender">Nadawca</option>
              <option value="recipient">Odbiorca</option>
            </select>
          </div>
        </div>

        <div className="filters-row-fixed">
          <div className="filter-section">
            <label htmlFor="filter-sender">Nadawca:</label>
            <input
              id="filter-sender"
              type="text"
              placeholder="Szukaj nadawcy..."
              value={filterSender}
              onChange={(e) => setFilterSender(e.target.value)}
              className="filter-input"
            />
          </div>

          <div className="filter-section">
            <label htmlFor="filter-recipient">Odbiorca:</label>
            <input
              id="filter-recipient"
              type="text"
              placeholder="Szukaj odbiorcy..."
              value={filterRecipient}
              onChange={(e) => setFilterRecipient(e.target.value)}
              className="filter-input"
            />
          </div>
        </div>

        <div className="filters-row-fixed">
          <div className="filter-section">
            <label htmlFor="filter-date-from">Data od:</label>
            <input
              id="filter-date-from"
              type="date"
              value={filterDateFrom}
              onChange={(e) => setFilterDateFrom(e.target.value)}
              className="filter-input"
            />
          </div>

          <div className="filter-section">
            <label htmlFor="filter-date-to">Data do:</label>
            <input
              id="filter-date-to"
              type="date"
              value={filterDateTo}
              onChange={(e) => setFilterDateTo(e.target.value)}
              className="filter-input"
            />
          </div>

          <div className="filter-actions">
            <button className="clear-filters-btn" onClick={clearFilters}>
              🔄 Wyczyść filtry
            </button>
            <button className="refresh-btn" onClick={fetchShipments}>
              ↻ Odśwież
            </button>
          </div>
        </div>
      </div>

      <div className="results-info">
        <p>Znaleziono: <strong>{filteredShipments.length}</strong> z {shipments.length} przesyłek</p>
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
                <th>Nadawca</th>
                <th>Odbiorca</th>
                <th>Kurier</th>
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
                  <td>{shipment.sender_fullname || shipment.sender_email || "—"}</td>
                  <td>{shipment.recipient_fullname || shipment.recipient_email || "—"}</td>
                  <td>{shipment.courier_id ? "Tak" : "Nie"}</td>
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
                        onClick={() => setStatusModalShipment(shipment)}
                        title="Zmień status"
                      >
                        ✏️
                      </button>
                      <button
                        className="btn-assign"
                        onClick={() => setCourierModalShipment(shipment)}
                        title="Przypisz kuriera"
                      >
                        👤
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

      {statusModalShipment && (
        <UpdatePackageStatusModal
          shipment={statusModalShipment}
          onClose={() => setStatusModalShipment(null)}
          onSuccess={fetchShipments}
        />
      )}

      {courierModalShipment && (
        <AssignCourierModal
          shipment={courierModalShipment}
          onClose={() => setCourierModalShipment(null)}
          onSuccess={fetchShipments}
        />
      )}
    </div>
  );
}
