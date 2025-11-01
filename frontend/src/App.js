import React, { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [city, setCity] = useState("Accra");
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchWeather = async (cityName) => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/weather?city=${cityName}`
      );

      if (!response.ok) {
        throw new Error("Failed to fetch weather data");
      }

      const data = await response.json();
      setWeather(data);
    } catch (err) {
      setError(err.message);
      setWeather(null);
    } finally {
      setLoading(false);
    }
  };

  // Fetch Accra on first load
  useEffect(() => {
    fetchWeather("Accra");
  }, []);

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      fetchWeather(city);
    }
  };

  return (
    <div className="app">
      <h1>🌤 Weather App</h1>

      <div className="search-bar">
        <input
          type="text"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Enter any city (e.g. Accra, London, Tokyo...)"
        />
        <button onClick={() => fetchWeather(city)}>Get Weather</button>
      </div>

      {loading && <p>Loading weather...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {weather && (
        <div className="weather-card">
          <h2>{weather.city}</h2>
          <p>{weather.description}</p>
          <p>🌡 Temp: {weather.temperature} °C</p>
          <p>💧 Humidity: {weather.humidity}%</p>
          <p>💨 Wind: {weather.wind_speed} m/s</p>
          <p>
            <strong>{weather.weather_main}</strong> – {weather.description}
          </p>
          <div className="weather-icon">
            <img
              src={`https://openweathermap.org/img/wn/${weather.icon}@4x.png`}
              alt={weather.description}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
