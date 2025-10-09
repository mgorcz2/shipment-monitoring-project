import React, { useState, useEffect } from "react";
import { getAllUsers } from "../services/userService";
import UserList from "../components/UsersTable";
import UserDetailsModal from "../components/UserDetailsModal";
import "../styles/AdminPanel.css";

const AdminPanel = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedUser, setSelectedUser] = useState(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await getAllUsers();
      setUsers(response.data);
    } catch (err) {
      console.error("Błąd podczas pobierania użytkowników:", err);
      setError("Nie udało się pobrać listy użytkowników");
    } finally {
      setLoading(false);
    }
  };

  const handleViewDetails = (user) => {
    setSelectedUser(user);
  };

  const handleEditUser = (user) => {
    alert(`Funkcja edycji użytkownika ${user.email} zostanie zaimplementowana później`);
  };

  const handleDeleteUser = (user) => {
    if (window.confirm(`Czy na pewno chcesz usunąć użytkownika ${user.email}?`)) {
      alert(`Funkcja usuwania użytkownika zostanie zaimplementowana później`);
    }
  };

  const closeDetailsModal = () => {
    setSelectedUser(null);
  };

  return (
    <div className="admin-panel">
      <div className="admin-header">
        <h1>Panel Administratora</h1>
        <p>Zarządzanie użytkownikami systemu</p>
      </div>

      {loading ? (
        <div className="loading-state">Ładowanie użytkowników...</div>
      ) : error ? (
        <div className="error-state">{error}</div>
      ) : (
        <UserList
          users={users}
          onViewDetails={handleViewDetails}
          onEditUser={handleEditUser}
          onDeleteUser={handleDeleteUser}
        />
      )}

      {selectedUser && (
        <UserDetailsModal user={selectedUser} onClose={closeDetailsModal} />
      )}
    </div>
  );
};

export default AdminPanel;