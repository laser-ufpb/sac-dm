import { useEffect } from "react";
import DeviceService from "../../app/services/devices";

export const Home = () => {
  useEffect(() => {
    loadDevices();
  }, []);

  const loadDevices = async () => {
    try {
      await DeviceService.getDevices();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h1>Home</h1>
    </div>
  );
};
