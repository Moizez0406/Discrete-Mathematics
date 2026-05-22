const TOKEN = "7fb87bac252dd4e6e15f8db04838a8ca99387b54";
const BBOX = "41.30,1.95,41.50,2.30";

let RADIUS_KM = 5;

const map = L.map("map").setView([41.39, 2.15], 12);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "&copy; OpenStreetMap contributors",
}).addTo(map);

let stations = [];
let markers = [];
let edges = [];
let edgeConnections = [];

function getColor(aqi) {
  const v = parseInt(aqi);
  if (isNaN(v) || v < 0) return "#777";
  if (v <= 50) return "#00FFFF";
  if (v <= 100) return "#EE4B2B";
  if (v <= 150) return "#EE4B2B";
  return "#8B0000";
}

function getDistance(lat1, lon1, lat2, lon2) {
  const R = 6371;
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLon = ((lon2 - lon1) * Math.PI) / 180;
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLon / 2) ** 2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

function buildGraph() {
  edges.forEach((e) => map.removeLayer(e));
  edges = [];
  edgeConnections = [];

  for (let i = 0; i < stations.length; i++) {
    for (let j = i + 1; j < stations.length; j++) {
      const dist = getDistance(
        stations[i].lat,
        stations[i].lon,
        stations[j].lat,
        stations[j].lon,
      );

      if (dist <= RADIUS_KM) {
        const line = L.polyline(
          [
            [stations[i].lat, stations[i].lon],
            [stations[j].lat, stations[j].lon],
          ],
          { color: "#ffffff", weight: 1.2, opacity: 0.35 },
        ).addTo(map);
        edges.push(line);
        edgeConnections.push({
          line: line,
          fromIdx: i,
          toIdx: j,
        });
      }
    }
  }

  updateNetworkStats();
}

function getNeighbors() {
  const neighbors = Array(stations.length)
    .fill()
    .map(() => []);
  for (let conn of edgeConnections) {
    neighbors[conn.fromIdx].push(conn.toIdx);
    neighbors[conn.toIdx].push(conn.fromIdx);
  }
  return neighbors;
}

function isConnected() {
  if (stations.length === 0) return false;

  const visited = new Array(stations.length).fill(false);
  const queue = [0];
  visited[0] = true;
  const neighbors = getNeighbors();

  while (queue.length > 0) {
    const current = queue.shift();
    for (let neighbor of neighbors[current]) {
      if (!visited[neighbor]) {
        visited[neighbor] = true;
        queue.push(neighbor);
      }
    }
  }

  return visited.every((v) => v === true);
}

function updateNetworkStats() {
  const numVertices = stations.length;
  const numEdges = edges.length;
  const maxEdges = (numVertices * (numVertices - 1)) / 2;
  const density = maxEdges > 0 ? ((numEdges / maxEdges) * 100).toFixed(2) : 0;
  const connected = isConnected();

  document.getElementById("statVertices").textContent = numVertices;
  document.getElementById("statEdges").textContent = numEdges;
  document.getElementById("statDensity").textContent = density + "%";

  const connectedEl = document.getElementById("statConnected");
  connectedEl.textContent = connected ? "Yes" : "No";
  connectedEl.style.color = connected ? "#22c55e" : "#ef4444";
}

function resetEdges() {
  for (let conn of edgeConnections) {
    conn.line.setStyle({ color: "#ffffff", weight: 1.2, opacity: 0.35 });
  }
}

function resetColors() {
  for (let i = 0; i < stations.length; i++) {
    markers[i].setStyle({ fillColor: getColor(stations[i].aqi), radius: 7 });
  }
  resetEdges();
}

function runDFS() {
  resetColors();
  resetEdges();

  if (stations.length === 0) return;

  const visited = new Array(stations.length).fill(false);
  const visitOrder = [];
  const usedEdges = new Set();

  function goDeeper(vertex) {
    visited[vertex] = true;
    visitOrder.push(vertex);
    markers[vertex].setStyle({ fillColor: "#AA6DC9", radius: 8 });

    for (let i = 0; i < stations.length; i++) {
      if (!visited[i]) {
        const dist = getDistance(
          stations[vertex].lat,
          stations[vertex].lon,
          stations[i].lat,
          stations[i].lon,
        );
        if (dist <= RADIUS_KM) {
          const edgeKey = vertex < i ? `${vertex}-${i}` : `${i}-${vertex}`;
          usedEdges.add(edgeKey);
          goDeeper(i);
        }
      }
    }
  }

  goDeeper(0);

  for (let conn of edgeConnections) {
    const key =
      conn.fromIdx < conn.toIdx
        ? `${conn.fromIdx}-${conn.toIdx}`
        : `${conn.toIdx}-${conn.fromIdx}`;
    if (usedEdges.has(key)) {
      conn.line.setStyle({ color: "#AA6DC9", weight: 3, opacity: 0.9 });
    }
  }
}

function runBFS() {
  resetColors();
  resetEdges();

  if (stations.length === 0) return;

  const visited = new Array(stations.length).fill(false);
  const queue = [0];
  visited[0] = true;
  const visitOrder = [];
  const usedEdges = new Set();

  while (queue.length) {
    const current = queue.shift();
    visitOrder.push(current);
    markers[current].setStyle({ fillColor: "#FF8C42", radius: 8 });

    for (let i = 0; i < stations.length; i++) {
      if (!visited[i]) {
        const dist = getDistance(
          stations[current].lat,
          stations[current].lon,
          stations[i].lat,
          stations[i].lon,
        );
        if (dist <= RADIUS_KM) {
          visited[i] = true;
          queue.push(i);
          const edgeKey = current < i ? `${current}-${i}` : `${i}-${current}`;
          usedEdges.add(edgeKey);
        }
      }
    }
  }

  for (let conn of edgeConnections) {
    const key =
      conn.fromIdx < conn.toIdx
        ? `${conn.fromIdx}-${conn.toIdx}`
        : `${conn.toIdx}-${conn.fromIdx}`;
    if (usedEdges.has(key)) {
      conn.line.setStyle({ color: "#FF8C42", weight: 3, opacity: 0.9 });
    }
  }
}

async function loadStations() {
  try {
    const res = await fetch(
      `https://api.waqi.info/map/bounds/?latlng=${BBOX}&token=${TOKEN}`,
    );
    const data = await res.json();

    if (data.status !== "ok") {
      throw new Error("API returned: " + data.status);
    }

    stations = data.data
      .filter((s) => s.lat && s.lon)
      .map((s) => ({
        lat: parseFloat(s.lat),
        lon: parseFloat(s.lon),
        name: s.station.name,
        aqi: s.aqi,
      }));

    markers.forEach((m) => map.removeLayer(m));
    markers = [];

    for (let s of stations) {
      const marker = L.circleMarker([s.lat, s.lon], {
        radius: 7,
        fillColor: getColor(s.aqi),
        color: "#fff",
        weight: 1,
        fillOpacity: 0.9,
      }).addTo(map);
      marker.bindPopup(`<b>${s.name}</b><br>AQI: ${s.aqi}`);
      markers.push(marker);
    }

    if (markers.length > 0) {
      const group = L.featureGroup(markers);
      map.fitBounds(group.getBounds().pad(0.1));
    }

    buildGraph();
    document.getElementById("loading").style.display = "none";
  } catch (err) {
    console.error(err);
    document.getElementById("loading").innerHTML =
      "Error loading sensors. Check token/network.";
    document.getElementById("loading").style.backgroundColor = "#ffcccc";
  }
}

document.getElementById("radius").addEventListener("input", (e) => {
  RADIUS_KM = parseFloat(e.target.value);
  document.getElementById("radiusVal").textContent = RADIUS_KM + " km";
  buildGraph();
  resetColors();
});

document.getElementById("brightness").addEventListener("input", (e) => {
  const v = parseFloat(e.target.value);
  document.documentElement.style.setProperty("--map-brightness", v);
  document.getElementById("brightVal").textContent = v.toFixed(2);
});

document.getElementById("dfsBtn").addEventListener("click", runDFS);
document.getElementById("bfsBtn").addEventListener("click", runBFS);

loadStations();
