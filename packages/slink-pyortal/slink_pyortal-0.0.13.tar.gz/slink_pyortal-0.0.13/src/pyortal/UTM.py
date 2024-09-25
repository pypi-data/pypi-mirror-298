import requests, datetime

class UTM(object):
	def __init__(self, base_url, cloud_uri):
		self.__base_url = base_url
		self.__cloud_uri = cloud_uri


	########## Simulator Management ##########
	def list_simulators(self):
		response = requests.get(f"http://{self.__base_url}/simulators")
		simulators = {}

		if response.status_code == 200:
			simulators = response.json()

		return simulators


	########## Vertiport Management ##########
	def list_vertiports(self):
		print(f"{self.__cloud_uri}/vertiports")
		response = requests.get(f"{self.__cloud_uri}/vertiports")
		vertiports = {}

		if response.status_code == 200:
			for vertiport in response.json():
				vertiports[vertiport["name"]] = vertiport

		return vertiports


	########## Vehicle Management ##########
	def spawn_vehicle(self, registration, spawn_point, cloud_id = None):
		simulator = self.list_simulators()[0]

		response = requests.post(
			f"http://{self.__base_url}/managed-vehicles",
			json={
				"simulator": simulator["self"],
				"registration": registration,
				"spawn_point": spawn_point,
				"cloud_id": cloud_id
			}
		)

		return response.status_code == 201

	def despawn_vehicle(self, registration):
		response = requests.delete(f"http://{self.__base_url}/vehicles/{registration}")
		return response.status_code == 200


	########## Flight Path Management ##########
	def create_flight_path(self, name, registration, origin, destination, waypoints):
		vertiports = self.list_vertiports()

		response = requests.post(
			f"http://{self.__base_url}/flight-paths",
			json={
			  "name": name,
			  "vehicle": registration,
			  "origin_id": vertiports[origin]["id"],
			  "destination_id": vertiports[destination]["id"],
			  "waypoints": waypoints
			}
		)

		return response.status_code == 201

	def remove_flight_path(self, name):
		response = requests.delete(f"http://{self.__base_url}/flight-paths/{name}")
		return response.status_code == 200


	########## Flight Management ##########
	def book_flight(self, vehicle, type, origin, destination, departure=None, round_trip=False):
		vertiports = self.list_vertiports()
		mission_types = {
			"delivery": "4",
			"charging": "5",
			"flight_only": "6"
		}

		vertiports = self.list_vertiports()

		payload = {
		  "vehicle": f"http://{self.__base_url}/vehicles/{vehicle}",
		  "mission_type": mission_types[type],
		  "origin": vertiports[origin]["id"],
		  "destination": vertiports[destination]["id"],
		  "round_trip": round_trip
		}

		if departure:
			payload["departure"] = departure.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

		response = requests.post(f"http://{self.__base_url}/queries", json=payload)

		if response.status_code != 201:
			return False

		query = response.json()

		if len(query["options"]) == 0:
			return None
			
		response = requests.post(
			f"http://{self.__base_url}/reservations",
			json={
			  "query_option": query["options"][0]["number"]
			}
		)

		if response.status_code == 201:
			return response.json()
		else:
			requests.delete(query["self"])
			return None


	def cancel_flight(self, flight):
		response = requests.delete(flight["self"])
		return response.status_code == 200
