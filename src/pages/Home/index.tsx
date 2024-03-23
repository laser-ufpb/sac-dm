import { useEffect, useState } from "react";
import DeviceService from "../../app/services/devices";
import AccelerometerService from "../../app/services/accelerometer";
import { CircularProgress } from "@mui/material";
import { Container } from "./styles";

export const Home = () => {
  const loadAccelerometers = async () => {
    try {
      await AccelerometerService.getAccelerometers();
    } catch (error) {
      console.error(error);
    } finally {
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
      <h1>Home</h1>
    </Container>
  );
};
