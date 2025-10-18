// Tek seferlik global tanımlar
const map = L.map("map").setView([39.9, 32.8], 6); // Türkiye merkez
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "© OpenStreetMap"
}).addTo(map);

// Uçak ikonu
const planeIcon = L.icon({
  iconUrl: "/static/img/plane.png",
  iconSize: [30, 30],
  iconAnchor: [15, 15]
});

// Marker listesi
const markers = {};

// SocketIO bağlantısı
const socket = io();

// Uçak verisi geldiğinde
socket.on("aircraft_data", function(data) {
  data.forEach(ac => {
    if (!ac.lat || !ac.lon) return;

    const id = ac.hex;
    const pos = [ac.lat, ac.lon];

    if (!markers[id]) {
      markers[id] = L.marker(pos, {icon: planeIcon}).addTo(map);
    } else {
      markers[id].setLatLng(pos);
    }

    // Tooltip ile hız/irtifa
    let info = `HEX: ${id}<br>`;
    if (ac.alt_baro) info += `Alt: ${ac.alt_baro} ft<br>`;
    if (ac.gs) info += `Hız: ${ac.gs} kt`;
    markers[id].bindTooltip(info);
  });
});
