import { api } from "..";

interface Vehicle {
  model: string;
  manufacturer: string;
  manufacture_year: number;
  engine_type: string;
  number_of_engines: number;
}

class VehicleService {
  async getVehicles() {
    try {
      const response = await api.get("/vehicle");
      return response.data;
    } catch (error) {
      console.error(error);
    }
  }

  async getVehicleById(id: number) {
    try {
      const response = await api.get(`/vehicle_by_id/${id}`);
      return response.data;
    } catch (error) {
      console.error(error);
    }
  }

  async postVehicle(vehicle: Vehicle) {
    try {
      const response = await api.post("/vehicle", {
        ...vehicle,
        status_id: 1,
      });
      return response.data;
    } catch (error) {
      console.error(error);
    }
  }
}

const vehicleService = new VehicleService();
export default vehicleService;
