import { api } from "..";
import { AccelerometerPayload } from "./types";

class AccelerometerService {
  getAccelerometers = async () => {
    try {
      const response = await api.get("/accelerometer");
      console.log(response);
    } catch (error) {
      console.error(error);
    }
  };

  postAccelerometers = async (payload: AccelerometerPayload) => {
    try {
      const response = await api.post("/accelerometer", payload);
      console.log(response);
    } catch (error) {
      console.error(error);
    }
  };
}

export default new AccelerometerService();
