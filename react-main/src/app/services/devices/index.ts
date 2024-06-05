import { api } from "..";
import { DevicePayload } from "./types";

class DeviceService {
  async getDevices() {
    try {
      const response = await api.get("/device");
      return response.data;
    } catch (error) {
      console.error(error);
    }
  }

  async postDevices(payload: DevicePayload) {
    try {
      const response = await api.post("/device", {
        ...payload,
        status_id: 1,
      });
      console.log(response);
    } catch (error) {
      console.error(error);
    }
  }
}

const deviceService = new DeviceService();
export default deviceService;
