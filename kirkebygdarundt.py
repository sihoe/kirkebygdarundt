import gpxpy
import requests
import time
import json

def get_elevation(lat, lon):
    url = f"https://api.opentopodata.org/v1/eudem25m?locations={lat},{lon}"
    try:
        response = requests.get(url)
        if response.status_code == 429:
            print("⚠️  For mange forespørsler – venter 5 sekunder...")
            time.sleep(5)
            return get_elevation(lat, lon)
        elif response.status_code != 200:
            print(f"❌ Feil: {response.status_code}")
            return None
        data = response.json()
        return data['results'][0]['elevation']
    except Exception as e:
        print(f"❌ Feil ved henting: {e}")
        return None

def hent_og_lagre_hoyde_spor(gpx_fil, json_fil):
    with open(gpx_fil, 'r') as f:
        gpx = gpxpy.parse(f)

    data = []
    teller = 0

    print("🔍 Fant spor (<trkpt>) – starter innhenting...")
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                teller += 1
                print(f"Henter punkt {teller}: ({point.latitude}, {point.longitude})")
                ele = get_elevation(point.latitude, point.longitude)
                data.append({
                    "lat": point.latitude,
                    "lon": point.longitude,
                    "ele": ele
                })
                time.sleep(1)

    with open(json_fil, 'w') as outfile:
        json.dump(data, outfile, indent=2)
        print(f"\n✅ Ferdig! Lagret {len(data)} punkter til {json_fil}")

if __name__ == "__main__":
    hent_og_lagre_hoyde_spor("kirkebydgarundt.gpx", "kirkebygdarundt_elevation.json")
