import React, { useState } from "react";
import { FaSort, FaSortUp, FaSortDown, FaEdit, FaInfoCircle, FaTrash } from "react-icons/fa";
import "../styles/AdminPanel.css";
import { useNavigate } from "react-router-dom";

const UserList = ({ users, onViewDetails, onDeleteUser, onEditUser }) => {
  const [sortField, setSortField] = useState("created_at");
  const [sortDirection, setSortDirection] = useState("desc");
  const [roleFilter, setRoleFilter] = useState("all");


  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortDirection("asc");
    }
  };

  const getSortIcon = (field) => {
    if (sortField !== field) return <FaSort />;
    return sortDirection === "asc" ? <FaSortUp /> : <FaSortDown />;
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };


  const filteredUsers = users.filter(
    (user) => roleFilter === "all" || user.role === roleFilter
  );


  const sortedUsers = [...filteredUsers].sort((a, b) => {
    if (sortField === "created_at") {
      const dateA = new Date(a[sortField]).getTime();
      const dateB = new Date(b[sortField]).getTime();
      return sortDirection === "asc" ? dateA - dateB : dateB - dateA;
    }
    
    if (a[sortField] < b[sortField]) return sortDirection === "asc" ? -1 : 1;
    if (a[sortField] > b[sortField]) return sortDirection === "asc" ? 1 : -1;
    return 0;
  });

  return (
    <div className="user-list-container">
      <div className="filter-bar">
        <div className="filter-group">
          <label htmlFor="role-filter">Filtruj według roli:</label>
          <select
            id="role-filter"
            className="filter-select"
            value={roleFilter}
            onChange={(e) => setRoleFilter(e.target.value)}
          >
            <option value="all">Wszyscy użytkownicy</option>
            <option value="admin">Administratorzy</option>
            <option value="client">Klienci</option>
            <option value="courier">Kurierzy</option>
            <option value="manager">Managerowie</option>
          </select>
        </div>
      </div>

      <div className="table-container">
        <table className="user-table">
          <thead>
            <tr>
              <th onClick={() => handleSort("email")}>
                Email {getSortIcon("email")}
              </th>
              <th onClick={() => handleSort("role")}>
                Rola {getSortIcon("role")}
              </th>
              <th onClick={() => handleSort("created_at")}>
                Data utworzenia {getSortIcon("created_at")}
              </th>
              <th>Akcje</th>
            </tr>
          </thead>
          <tbody>
            {sortedUsers.length === 0 ? (
              <tr>
                <td colSpan="4" className="no-data">
                  Brak użytkowników spełniających kryteria
                </td>
              </tr>
            ) : (
              sortedUsers.map((user) => (
                <tr key={user.id}>
                  <td>{user.email}</td>
                  <td>
                    <span className={`role-badge role-${user.role}`}>
                      {user.role}
                    </span>
                  </td>
                  <td>{formatDate(user.created_at)}</td>
                  <td>
                    <div className="action-buttons">
                      <button
                        className="action-btn details-btn"
                        onClick={() => onViewDetails(user)}
                        title="Szczegóły"
                      >
                        <FaInfoCircle />
                      </button>
                      <button
                        className="action-btn edit-btn"
                        onClick={() => onEditUser(user)}
                        title="Edytuj"
                      >
                        <FaEdit />
                      </button>
                      <button
                        className="action-btn delete-btn"
                        onClick={() => onDeleteUser(user)}
                        title="Usuń"
                      >
                        <FaTrash />
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default UserList;