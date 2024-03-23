import { api } from "..";
import { DevicePayload } from "./types";

class DeviceService {
  constructor() {}

  getDevices = async () => {
    try {
      const response = await api.get("/device");
      return response.data;
    } catch (error) {
      console.error(error);
    }
  };

  postDevices = async (payload: DevicePayload) => {
    try {
      const response = await api.post("/device", payload);
      console.log(response);
    } catch (error) {
      console.error(error);
    }
  };
}

export default new DeviceService();
