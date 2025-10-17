import React, { useState, useEffect, useRef } from "react";
import "../styles/ShipmentsPage.css";
import { translate } from "../i18n";
import { getPackageByShipmentId } from "../services/packageService";
// Importy dla map
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

// Konfiguracja ikon dla markerów
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

// Ikony dla punktów nadania i odbioru
const originIcon = new L.Icon({
  iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const destinationIcon = new L.Icon({
  iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

// Komponent, który dopasuje widok mapy do markerów
function MapBoundsAdjuster({ coords }) {
  const map = useMap();
  
  useEffect(() => {
    if (coords && coords.length > 0) {
      // Tworzymy bounds z wszystkich dostępnych współrzędnych
      const bounds = L.latLngBounds(coords);
      
      // Dopasuj widok mapy z marginesem
      map.fitBounds(bounds, {
        padding: [50, 50], // Dodaj margines 50px
        maxZoom: 15        // Ogranicz maksymalny zoom
      });
    }
  }, [coords, map]);
  
  return null;
}

export default function ShipmentDetailsModal({ shipment, onClose }) {
  const [packageDetails, setPackageDetails] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [mapReady, setMapReady] = useState(false);
  const mapRef = useRef(null);
  
  // Sprawdź, czy są dostępne koordynaty - używając nowego formatu danych
  const hasOriginCoords = shipment?.origin_coords && shipment.origin_coords.length === 2;
  const hasDestinationCoords = shipment?.destination_coords && shipment.destination_coords.length === 2;
  const hasCoords = hasOriginCoords || hasDestinationCoords;
  
  // Przygotuj tablicę wszystkich współrzędnych dla bounds
  const allCoords = [];
  if (hasOriginCoords) {
    allCoords.push([shipment.origin_coords[0], shipment.origin_coords[1]]);
  }
  if (hasDestinationCoords) {
    allCoords.push([shipment.destination_coords[0], shipment.destination_coords[1]]);
  }
  
  // Oblicz środek mapy używając nowego formatu danych
  const center = hasCoords ? [
    hasOriginCoords ? shipment.origin_coords[0] : shipment.destination_coords[0],
    hasOriginCoords ? shipment.origin_coords[1] : shipment.destination_coords[1]
  ] : [52.2297, 21.0122]; // Domyślnie Warszawa

  useEffect(() => {
    if (shipment?.id) {
      fetchPackageDetails(shipment.id);
    }
    
    console.log("Dane przesyłki:", {
      shipment: shipment,
      origin_coords: shipment?.origin_coords,
      destination_coords: shipment?.destination_coords,
      hasOriginCoords,
      hasDestinationCoords,
      hasCoords,
      center,
      allCoords
    });
    
    const timer = setTimeout(() => {
      setMapReady(true);
    }, 300);
    
    return () => clearTimeout(timer);
  }, [shipment]);

  useEffect(() => {
    if (mapReady && mapRef.current) {
      setTimeout(() => {
        mapRef.current.invalidateSize();
      }, 100);
    }
  }, [mapReady]);

  const fetchPackageDetails = async (shipmentId) => {
    setLoading(true);
    setError(null);
    try {
      const response = await getPackageByShipmentId(shipmentId);
      setPackageDetails(response.data);
    } catch (err) {
      console.error("Nie udało się pobrać szczegółów paczki:", err);
      setError("Nie udało się pobrać szczegółów paczki");
    } finally {
      setLoading(false);
    }
  };

  if (!shipment) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button className="modal-close-btn" onClick={onClose}>×</button>
        
        <h2>Szczegóły przesyłki #{shipment.id}</h2>
        <div className="shipment-details">
          <div className="detail-row">
            <span className="detail-label">Status:</span>
            <span className={`status-badge status-${shipment.status?.toLowerCase()}`}>
              {translate(shipment.status)}
            </span>
          </div>
          <div className="detail-row">
            <span className="detail-label">Nadawca:</span>
            <span>{shipment.sender_fullname || "Nieznany"}</span>
          </div>
          <div className="detail-row">
            <span className="detail-label">Odbiorca:</span>
            <span>{shipment.recipient_fullname || shipment.recipient_email || "Nieznany"}</span>
          </div>
          <div className="detail-row">
            <span className="detail-label">Adres nadania:</span>
            <span>{shipment.origin}</span>
          </div>
          <div className="detail-row">
            <span className="detail-label">Adres odbioru:</span>
            <span>{shipment.destination}</span>
          </div>
          
          {!hasCoords && (
            <div className="no-coords-message">
              <p>Brak współrzędnych geograficznych dla tej przesyłki.</p>
            </div>
          )}
          
          {hasCoords && mapReady && (
            <div className="shipment-map-container">
              <h3 className="map-title">Mapa adresów nadania i odbioru</h3>
              <MapContainer 
                key={`map-${shipment.id}`}
                center={center}
                zoom={9}
                className="shipment-map"
                whenCreated={(mapInstance) => {
                  mapRef.current = mapInstance;
                  setTimeout(() => {
                    mapInstance.invalidateSize();
                  }, 100);
                }}
              >
                <TileLayer
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  attribution="&copy; OpenStreetMap contributors"
                />
                
                
                <MapBoundsAdjuster coords={allCoords} />
                
                {hasOriginCoords && (
                  <Marker 
                    position={[shipment.origin_coords[0], shipment.origin_coords[1]]}
                    icon={originIcon}
                  >
                    <Popup>
                      <b>Miejsce nadania</b><br />
                      {shipment.origin}
                    </Popup>
                  </Marker>
                )}
                
                {hasDestinationCoords && (
                  <Marker 
                    position={[shipment.destination_coords[0], shipment.destination_coords[1]]}
                    icon={destinationIcon}
                  >
                    <Popup>
                      <b>Miejsce odbioru</b><br />
                      {shipment.destination}
                    </Popup>
                  </Marker>
                )}
              </MapContainer>
            </div>
          )}
          
          <div className="detail-row">
            <span className="detail-label">Data utworzenia:</span>
            <span>{new Date(shipment.created_at).toLocaleString()}</span>
          </div>
          {shipment.courier_id && (
            <div className="detail-row">
              <span className="detail-label">ID kuriera:</span>
              <span>{shipment.courier_id}</span>
            </div>
          )}
          
     
          <h3 className="package-details-title">Szczegóły paczki</h3>
          
          {loading ? (
            <p className="loading-text">Ładowanie szczegółów paczki...</p>
          ) : error ? (
            <p className="error-text">{error}</p>
          ) : packageDetails ? (
            <div className="package-details">
              <div className="detail-row">
                <span className="detail-label">Waga:</span>
                <span>{packageDetails.weight} kg</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Wymiary:</span>
                <span>{packageDetails.length} × {packageDetails.width} × {packageDetails.height} cm</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Zawartość delikatna:</span>
                <span>{packageDetails.fragile ? "Tak" : "Nie"}</span>
              </div>
            </div>
          ) : (
            <p className="no-package-text">Brak informacji o paczce</p>
          )}
        </div>
      </div>
    </div>
  );
}