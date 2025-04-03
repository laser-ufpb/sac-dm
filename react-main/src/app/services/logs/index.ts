
import { api } from "..";

class LogsVehicle {
    async getLogs(vehicleId: number) {
      try {
        const response = await api.get(`/log_by_vehicle_id/${vehicleId}`);
        return response.data;
      } catch (error) {
        console.error(error);
      }
    }
  }
  

const logsVehicle = new LogsVehicle();
export default logsVehicle;