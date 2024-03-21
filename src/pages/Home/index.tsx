import { useEffect, useState } from "react";
import DeviceService from "../../app/services/devices";
import AccelerometerService from "../../app/services/accelerometer";
import { CircularProgress } from "@mui/material";
import { Container } from "./styles";

export const Home = () => {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadDevices();
    // loadAccelerometers();
  }, []);

  const loadDevices = async () => {
    setIsLoading(true);
    try {
      await DeviceService.getDevices();
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadAccelerometers = async () => {
    setIsLoading(true);
    try {
      await AccelerometerService.getAccelerometers();
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const postDevices = async () => {
    const payload = "JV7";
    try {
      await DeviceService.postDevices({ device_code: payload });
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Container>
      {isLoading ? (
        <CircularProgress />
      ) : (
        <>
          <h1>Home</h1>
        </>
      )}
    </Container>
  );
};
