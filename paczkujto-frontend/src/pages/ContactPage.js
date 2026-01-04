import React from "react";
import logo from "../assets/logo.png";
import "../styles/HomePage.css";

export default function ContactPage() {
  return (
    <div className="home-container">
      <img src={logo} alt="Logo" className="home-logo" />
      <h1 className="home-title">Kontakt</h1>
      <p style={{ color: "#444", marginBottom: 24, fontSize: 18, textAlign: "center" }}>
        Masz pytania o przesyłkę, nadanie paczki lub panel użytkownika? Napisz lub zadzwoń.
      </p>

      <div
        style={{
          width: "100%",
          maxWidth: 720,
          background: "#fff",
          padding: 24,
          borderRadius: 8,
        }}
      >
        <h2 style={{ marginTop: 0, marginBottom: 12 }}>paczkuj.to</h2>

        <div style={{ display: "grid", gap: 10 }}>
          <div>
            <strong>Telefon:</strong> +48 123 456 789
          </div>
          <div>
            <strong>Email:</strong> kontakt@paczkuj.to
          </div>
          <div>
            <strong>Adres:</strong> ul. Przykładowa 1, 00-000 Warszawa
          </div>
          <div>
            <strong>Lokalizacja:</strong> Warszawa, Polska
          </div>
          <div>
            <strong>Godziny pracy:</strong> Pon–Pt 08:00–18:00
          </div>
        </div>

        <div style={{ display: "flex", gap: 16, marginTop: 20, flexWrap: "wrap" }}>
          <a className="btn btn-primary" href="mailto:kontakt@paczkuj.to">
            Napisz do nas
          </a>
          <a className="btn btn-primary" href="tel:+48123456789">
            Zadzwoń
          </a>
          <a
            className="btn btn-primary"
            href="https://maps.google.com/?q=Warszawa%2C%20Polska"
            target="_blank"
            rel="noreferrer"
          >
            Zobacz na mapie
          </a>
        </div>
      </div>
    </div>
  );
}
