export const geocodeAddress = async (address) => {
  try {
    const response = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`
    );
    const data = await response.json();
    
    if (data && data[0]) {
      return [parseFloat(data[0].lat), parseFloat(data[0].lon)];
    }
    return null;
  } catch (error) {
    console.error("Błąd geokodowania:", error);
    return null;
  }
};

export const formatAddress = (street, number, city, postcode) => {
  return `${street} ${number}, ${city}, ${postcode}`;
};