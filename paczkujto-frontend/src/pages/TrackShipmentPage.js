import React, { useEffect, useState } from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import axios from 'axios';
import ShipmentDetailsModal from '../components/ShipmentDetailsModal';

const TrackShipmentPage = () => {
  const { id } = useParams();
  const [searchParams] = useSearchParams();
  const email = searchParams.get('email');
  const [shipment, setShipment] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchShipment = async () => {
      try {
        if (!email) {
          setError('Brak adresu email w linku trackingowym.');
          setLoading(false);
          return;
        }
        const response = await axios.get(`http://localhost:8000/shipments/check_status`, {
          params: {
            shipment_id: id,
            recipient_email: email
          }
        });
        setShipment(response.data);
        setLoading(false);
      } catch (err) {
        setError('Nie znaleziono przesyłki lub nieprawidłowy adres email.');
        setLoading(false);
      }
    };

    fetchShipment();
  }, [id, email]);

  if (loading) {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f7f7f7' }}>
        <div>
          <p>Ładowanie...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f7f7f7' }}>
        <div>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f7f7f7' }}>
      {shipment && (
        <ShipmentDetailsModal
          shipment={shipment}
          onClose={() => window.location.href = '/'}
        />
      )}
    </div>
  );
};

export default TrackShipmentPage;
