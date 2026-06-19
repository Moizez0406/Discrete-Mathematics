const TOKEN = '7fb87bac252dd4e6e15f8db04838a8ca99387b54';
const BBOX = '41.30,1.95,41.50,2.30';

let RADIUS_KM = 9;

const map = L.map('map').setView([41.39, 2.15], 12);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

let stations = [];
let markers = [];
let edges = [];
let edgeConnections = [];

let currentPathLine = null;
let currentStartMarker = null;
let currentEndMarker = null;

function getColor(aqi) {
  const v = parseInt(aqi);
  if (isNaN(v) || v < 0) return '#777';
  if (v <= 50) return '#00FFFF';
  if (v <= 100) return '#EE4B2B';
  if (v <= 150) return '#EE4B2B';
  return '#8B0000';
}

function haversineKm(lat1, lon1, lat2, lon2) {
  const R = 6371;
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dLat/2)**2 +
    Math.cos(lat1*Math.PI/180) *
    Math.cos(lat2*Math.PI/180) *
    Math.sin(dLon/2)**2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
}

function buildGraph() {
  edges.forEach(e => map.removeLayer(e));
  edges = [];
  edgeConnections = [];

  for (let i = 0; i < stations.length; i++) {
    for (let j = i + 1; j < stations.length; j++) {
      const dist = haversineKm(
        stations[i].lat, stations[i].lon,
        stations[j].lat, stations[j].lon
      );

      if (dist <= RADIUS_KM) {
        const line = L.polyline(
          [[stations[i].lat, stations[i].lon],
           [stations[j].lat, stations[j].lon]],
          { color: '#ffffff', weight: 1.2, opacity: 0.35 }
        ).addTo(map);
        edges.push(line);
        edgeConnections.push({
          line: line,
          fromIdx: i,
          toIdx: j
        });
      }
    }
  }
  
  updateNetworkStats();
  updateSensorDropdowns();
}

function getNeighbors() {
  const neighbors = Array(stations.length).fill().map(() => []);
  for (let conn of edgeConnections) {
    neighbors[conn.fromIdx].push(conn.toIdx);
    neighbors[conn.toIdx].push(conn.fromIdx);
  }
  return neighbors;
}

function isGraphConnected() {
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
  
  return visited.every(v => v === true);
}

function updateNetworkStats() {
  const numVertices = stations.length;
  const numEdges = edges.length;
  const maxEdges = numVertices * (numVertices - 1) / 2;
  const density = maxEdges > 0 ? (numEdges / maxEdges * 100).toFixed(2) : 0;
  const connected = isGraphConnected();
  
  document.getElementById('statVertices').textContent = numVertices;
  document.getElementById('statEdges').textContent = numEdges;
  document.getElementById('statDensity').textContent = density + '%';
  
  const connectedEl = document.getElementById('statConnected');
  connectedEl.textContent = connected ? 'Yes' : 'No';
  connectedEl.style.color = connected ? '#22c55e' : '#ef4444';
}

function updateSensorDropdowns() {
  const selects = [sensor1, sensor2, sensor3, sensor4];
  
  for (let select of selects) {
    select.innerHTML = '';
  }
  
  for (let i = 0; i < stations.length; i++) {
    for (let select of selects) {
      const option = document.createElement('option');
      option.value = i;
      option.textContent = stations[i].name.length > 30 ? 
        stations[i].name.substring(0, 27) + '...' : stations[i].name;
      select.appendChild(option);
    }
  }
  
  if (stations.length >= 4) {
    sensor1.value = 0;
    sensor2.value = 1;
    sensor3.value = 2;
    sensor4.value = 3;
  }
}

// ============================================
// DEPTH FIRST SEARCH (DFS)
// ============================================

function runDFS() {
  resetColors();
  clearPathVisualization();
  
  if (stations.length === 0) return;
  
  const visited = new Array(stations.length).fill(false);
  const usedEdges = new Set();
  
  function goDeeper(vertex) {
    visited[vertex] = true;
    markers[vertex].setStyle({ fillColor: '#AA6DC9', radius: 8 });
    
    for (let i = 0; i < stations.length; i++) {
      if (!visited[i]) {
        const dist = haversineKm(
          stations[vertex].lat, stations[vertex].lon,
          stations[i].lat, stations[i].lon
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
    const key = conn.fromIdx < conn.toIdx ? `${conn.fromIdx}-${conn.toIdx}` : `${conn.toIdx}-${conn.fromIdx}`;
    if (usedEdges.has(key)) {
      conn.line.setStyle({ color: '#AA6DC9', weight: 3, opacity: 0.9 });
    }
  }
}

// ============================================
// BREADTH FIRST SEARCH (BFS)
// ============================================

function runBFS() {
  resetColors();
  clearPathVisualization();
  
  if (stations.length === 0) return;
  
  const visited = new Array(stations.length).fill(false);
  const queue = [0];
  visited[0] = true;
  const usedEdges = new Set();
  
  while (queue.length) {
    const current = queue.shift();
    markers[current].setStyle({ fillColor: '#FF8C42', radius: 8 });
    
    for (let i = 0; i < stations.length; i++) {
      if (!visited[i]) {
        const dist = haversineKm(
          stations[current].lat, stations[current].lon,
          stations[i].lat, stations[i].lon
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
    const key = conn.fromIdx < conn.toIdx ? `${conn.fromIdx}-${conn.toIdx}` : `${conn.toIdx}-${conn.fromIdx}`;
    if (usedEdges.has(key)) {
      conn.line.setStyle({ color: '#FF8C42', weight: 3, opacity: 0.9 });
    }
  }
}

// ============================================
// SIMULATED ANNEALING FOR SHORTEST ROUTE
// ============================================

function findShortestRoute(requiredSensors) {
  const neighbors = getNeighbors();

  function bfsPath(start, end) {
    const queue = [[start]];
    const visited = new Set([start]);
    while (queue.length > 0) {
      const path = queue.shift();
      const current = path[path.length - 1];
      if (current === end) return path;
      for (let neighbor of neighbors[current]) {
        if (!visited.has(neighbor)) {
          visited.add(neighbor);
          queue.push([...path, neighbor]);
        }
      }
    }
    return null;
  }

  function buildFullRoute(order) {
    let fullRoute = [];
    for (let i = 0; i < order.length - 1; i++) {
      const partial = bfsPath(order[i], order[i + 1]);
      if (!partial) return null;
      if (i === 0) {
        fullRoute.push(...partial);
      } else {
        fullRoute.push(...partial.slice(1));
      }
    }
    return fullRoute;
  }

  function routeDistance(route) {
    let total = 0;
    for (let i = 0; i < route.length - 1; i++) {
      total += haversineKm(
        stations[route[i]].lat, stations[route[i]].lon,
        stations[route[i + 1]].lat, stations[route[i + 1]].lon
      );
    }
    return total;
  }

  function swapMiddleSensors(perm) {
    if (perm.length <= 3) return;
    const i = 1 + Math.floor(Math.random() * (perm.length - 2));
    const j = 1 + Math.floor(Math.random() * (perm.length - 2));
    [perm[i], perm[j]] = [perm[j], perm[i]];
    return perm;
  }

  // Create initial random order for middle sensors
  let perm = [...requiredSensors];
  const middle = perm.slice(1, perm.length - 1);
  for (let i = middle.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [middle[i], middle[j]] = [middle[j], middle[i]];
  }
  perm = [perm[0], ...middle, perm[perm.length - 1]];

  let currentRoute = buildFullRoute(perm);
  if (!currentRoute) {
    return { path: null, distance: Infinity, error: 'No valid route exists!' };
  }

  let currentDist = routeDistance(currentRoute);
  let bestRoute = [...currentRoute];
  let bestDist = currentDist;
  let bestPerm = [...perm];

  let temp = 500;
  const coolingRate = 0.999;
  const iterations = 10000;

  for (let iter = 0; iter < iterations; iter++) {
    let candidatePerm = [...perm];
    swapMiddleSensors(candidatePerm);
    
    let candidateRoute = buildFullRoute(candidatePerm);
    if (!candidateRoute) continue;
    
    let candidateDist = routeDistance(candidateRoute);
    let delta = candidateDist - currentDist;
    
    if (delta < 0 || Math.random() < Math.exp(-delta / temp)) {
      perm = candidatePerm;
      currentRoute = candidateRoute;
      currentDist = candidateDist;
      
      if (currentDist < bestDist) {
        bestRoute = [...currentRoute];
        bestDist = currentDist;
        bestPerm = [...perm];
      }
    }
    
    temp *= coolingRate;
  }
  
  return { path: bestRoute, order: bestPerm, distance: bestDist, error: null };
}

// ============================================
// VISUALIZATION FUNCTIONS
// ============================================

function clearPathVisualization() {
  if (currentPathLine) map.removeLayer(currentPathLine);
  if (currentStartMarker) map.removeLayer(currentStartMarker);
  if (currentEndMarker) map.removeLayer(currentEndMarker);
  currentPathLine = null;
  currentStartMarker = null;
  currentEndMarker = null;
}

function visualizePath(selectedSensors, result) {
  clearPathVisualization();
  
  if (result.error || !result.path || result.path.length < 2) return;
  
  const pathPoints = result.path.map(idx => [stations[idx].lat, stations[idx].lon]);
  
  currentPathLine = L.polyline(pathPoints, {
    color: '#FF6B6B',
    weight: 5,
    opacity: 0.9,
    dashArray: '8, 6'
  }).addTo(map);
  
  const startIdx = selectedSensors[0];
  currentStartMarker = L.circleMarker([stations[startIdx].lat, stations[startIdx].lon], {
    radius: 12,
    fillColor: '#22c55e',
    color: '#fff',
    weight: 3,
    fillOpacity: 1
  }).addTo(map);
  currentStartMarker.bindPopup(`<b>START</b><br>${stations[startIdx].name}`);
  
  const endIdx = selectedSensors[selectedSensors.length - 1];
  currentEndMarker = L.circleMarker([stations[endIdx].lat, stations[endIdx].lon], {
    radius: 12,
    fillColor: '#ef4444',
    color: '#fff',
    weight: 3,
    fillOpacity: 1
  }).addTo(map);
  currentEndMarker.bindPopup(`<b>END</b><br>${stations[endIdx].name}`);
  
  const bounds = L.latLngBounds(pathPoints);
  map.fitBounds(bounds.pad(0.2));
}

function findAndShowRoute() {
  const s1 = parseInt(sensor1.value);
  const s2 = parseInt(sensor2.value);
  const s3 = parseInt(sensor3.value);
  const s4 = parseInt(sensor4.value);
  
  const selectedSensors = [s1, s2, s3, s4];
  const unique = new Set(selectedSensors);
  
  if (unique.size < 4) {
    alert('Please choose 4 different sensors!');
    return;
  }
  
  setTimeout(() => {
    const result = findShortestRoute(selectedSensors);
    visualizePath(selectedSensors, result);
  }, 50);
}

// ============================================
// HELPER FUNCTIONS
// ============================================

function resetColors() {
  for (let i = 0; i < stations.length; i++) {
    markers[i].setStyle({ fillColor: getColor(stations[i].aqi), radius: 7 });
  }
  for (let conn of edgeConnections) {
    conn.line.setStyle({ color: '#ffffff', weight: 1.2, opacity: 0.35 });
  }
}

// ============================================
// LOAD STATIONS
// ============================================

async function loadStations() {
  try {
    const res = await fetch(`https://api.waqi.info/map/bounds/?latlng=${BBOX}&token=${TOKEN}`);
    const data = await res.json();

    if (data.status !== 'ok') {
      throw new Error('API returned: ' + data.status);
    }

    stations = data.data.filter(s => s.lat && s.lon).map(s => ({
      lat: parseFloat(s.lat),
      lon: parseFloat(s.lon),
      name: s.station.name,
      aqi: s.aqi
    }));

    markers.forEach(m => map.removeLayer(m));
    markers = [];
    
    for (let i = 0; i < stations.length; i++) {
      const s = stations[i];
      const marker = L.circleMarker([s.lat, s.lon], {
        radius: 7,
        fillColor: getColor(s.aqi),
        color: '#fff',
        weight: 1,
        fillOpacity: 0.9
      }).addTo(map);
      marker.bindPopup(`<b>${s.name}</b><br>AQI: ${s.aqi}`);
      markers.push(marker);
    }

    if (markers.length > 0) {
      const group = L.featureGroup(markers);
      map.fitBounds(group.getBounds().pad(0.1));
    }

    buildGraph();
    document.getElementById('loading').style.display = 'none';
    
  } catch (err) {
    console.error(err);
    document.getElementById('loading').innerHTML = 'Error loading sensors.';
    document.getElementById('loading').style.backgroundColor = '#ffcccc';
  }
}

// ============================================
// EVENT LISTENERS
// ============================================

document.getElementById('radius').addEventListener('input', (e) => {
  RADIUS_KM = parseFloat(e.target.value);
  document.getElementById('radiusVal').textContent = RADIUS_KM + ' km';
  buildGraph();
  resetColors();
  clearPathVisualization();
});

document.getElementById('brightness').addEventListener('input', (e) => {
  const v = parseFloat(e.target.value);
  document.documentElement.style.setProperty('--map-brightness', v);
  document.getElementById('brightVal').textContent = v.toFixed(2);
});

document.getElementById('dfsBtn').addEventListener('click', runDFS);
document.getElementById('bfsBtn').addEventListener('click', runBFS);
document.getElementById('findPathBtn').addEventListener('click', findAndShowRoute);
document.getElementById('clearPathBtn').addEventListener('click', clearPathVisualization);

loadStations();
