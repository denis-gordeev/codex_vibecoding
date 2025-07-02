const map = L.map('map').setView([55.751244, 37.618423], 11);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

let overlayLayer;
let baseLayer;

async function geocode(city) {
  const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(city)}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error('Geocoding failed');
  const data = await res.json();
  if (!data.length) throw new Error('City not found');
  const c = data[0];
  const bbox = c.boundingbox.map(Number);
  return {lat: parseFloat(c.lat), lon: parseFloat(c.lon), bbox};
}

async function fetchRoads(bbox) {
  const query = `[out:json][timeout:25];(way["highway"](${bbox.join(',')}););out body;>;out skel qt;`;
  const res = await fetch('https://overpass-api.de/api/interpreter', {
    method: 'POST',
    body: query
  });
  if (!res.ok) throw new Error('Overpass request failed');
  const data = await res.json();
  return osmtogeojson(data);
}

function translateGeoJSON(geojson, dx, dy) {
  function translateCoords(coords) {
    for (let i = 0; i < coords.length; i++) {
      if (Array.isArray(coords[i][0])) {
        translateCoords(coords[i]);
      } else {
        coords[i][0] += dx;
        coords[i][1] += dy;
      }
    }
  }
  const copy = JSON.parse(JSON.stringify(geojson));
  copy.features.forEach(f => translateCoords(f.geometry.coordinates));
  return copy;
}

async function overlay() {
  const overlayCity = document.getElementById('overlayCity').value;
  const baseCity = document.getElementById('baseCity').value;
  if (!overlayCity || !baseCity) return alert('Please enter both cities');
  try {
    const [overlayInfo, baseInfo] = await Promise.all([geocode(overlayCity), geocode(baseCity)]);
    const [overlayRoads, baseRoads] = await Promise.all([fetchRoads(overlayInfo.bbox), fetchRoads(baseInfo.bbox)]);
    const dx = baseInfo.lon - overlayInfo.lon;
    const dy = baseInfo.lat - overlayInfo.lat;
    const movedOverlay = translateGeoJSON(overlayRoads, dx, dy);
    if (overlayLayer) map.removeLayer(overlayLayer);
    if (baseLayer) map.removeLayer(baseLayer);
    baseLayer = L.geoJSON(baseRoads, {color:'black', weight:1}).addTo(map);
    overlayLayer = L.geoJSON(movedOverlay, {color:'red', weight:1}).addTo(map);
    map.fitBounds(baseLayer.getBounds());
  } catch (err) {
    alert(err.message);
  }
}

document.getElementById('loadBtn').addEventListener('click', overlay);
