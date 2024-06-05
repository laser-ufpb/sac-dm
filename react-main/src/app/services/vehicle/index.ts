import { api } from "..";

class VehicleService {
  async getVehicles() {
    try {
      const response = await api.get("/vehicle");
      return response.data;
    } catch (error) {
      console.error(error);
    }
  }
}

const vehicleService = new VehicleService();
export default vehicleService;
