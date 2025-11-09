
import React, { useState, useEffect } from "react";
import { getAllUsers, deleteUser } from "../services/userService";  
import UserList from "../components/UsersTable";
import UserDetailsModal from "../components/UserDetailsModal";
import DeleteConfirmModal from "../components/DeleteConfirmModal"; 
import "../styles/AdminPanel.css";

const AdminPanel = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedUser, setSelectedUser] = useState(null);
  const [userToDelete, setUserToDelete] = useState(null);  
  const [isDeleting, setIsDeleting] = useState(false);      

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
    setUserToDelete(user);  
  };

  const confirmDelete = async () => {
    if (!userToDelete) return;

    setIsDeleting(true);
    try {
      await deleteUser(userToDelete.email);
      
      setUsers(users.filter(u => u.id !== userToDelete.id));
      
      alert(`✓ Użytkownik ${userToDelete.email} został usunięty`);
      
      setUserToDelete(null);
    } catch (err) {
      console.error("Błąd podczas usuwania:", err);
      alert(`✗ Błąd: ${err.response?.data?.detail || "Nie udało się usunąć użytkownika"}`);
    } finally {
      setIsDeleting(false);
    }
  };

  const cancelDelete = () => {
    setUserToDelete(null);
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

      {userToDelete && (
        <DeleteConfirmModal
          user={userToDelete}
          onConfirm={confirmDelete}
          onCancel={cancelDelete}
          isDeleting={isDeleting}
        />
      )}
    </div>
  );
};

export default AdminPanel;