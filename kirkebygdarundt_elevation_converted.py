import json
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # jordradius i meter
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = phi2 - phi1
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

with open("kirkebygdarundt_elevation.json", "r", encoding="utf-8") as f:
    data = json.load(f)

converted = []
distance = 0.0

for i, point in enumerate(data):
    lat = point["lat"]
    lon = point["lon"]
    ele = point["ele"]

    if i > 0:
        prev = data[i - 1]
        prev_lat = prev["lat"]
        prev_lon = prev["lon"]
        distance += haversine(prev_lat, prev_lon, lat, lon)

    converted.append({
        "distance": round(distance / 1000, 3),  # i km
        "elevation": ele
    })

with open("kirkebygdarundt_elevation_converted.json", "w", encoding="utf-8") as f:
    json.dump(converted, f, indent=2)

print("✅ Laget kirkebygdarundt_elevation_converted.json med", len(converted), "punkter.")