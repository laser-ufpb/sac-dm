import { api } from "..";
import { AccelerometerPayload } from "./types";

class AccelerometerService {
  async getAccelerometers() {
    try {
      const response = await api.get("/accelerometer");
      console.log(response);
    } catch (error) {
      console.error(error);
    }
  }

  async postAccelerometers(payload: AccelerometerPayload) {
    try {
      const response = await api.post("/accelerometer", payload);
      console.log(response);
    } catch (error) {
      console.error(error);
    }
  }
}

const accelerometerService = new AccelerometerService();
export default accelerometerService;
