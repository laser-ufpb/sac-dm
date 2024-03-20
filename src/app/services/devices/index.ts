import { api } from "..";

class DeviceService {
  constructor() {}

  getDevices = async () => {
    try {
      const response = await api.get("/device");
      console.log(response);
    } catch (error) {
      console.error(error);
    }
  };
}

export default new DeviceService();
