import { useParams } from "react-router-dom";
import { useEffect, useState, useCallback } from "react";
import { SacDmProps } from "../SacDm/types";
import { Description } from "./styles";
import { SacDmDevice } from "./components/SacDmDevice";
import mocksacdm from "../../mock/sacdm.json";
import { formatTime } from "../../utils/formatTime";

export const Device = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [deviceData, setDeviceData] = useState<SacDmProps[]>([]);

  const { id } = useParams();
  const numericId = Number(id);

  const loadSacDm = useCallback(async () => {
    setIsLoading(true);
    const formattedResponse = mocksacdm.map((item: SacDmProps) => ({
      ...item,
      timestamp: formatTime(item.timestamp),
    }));
    const filteredData = formattedResponse.filter(
      (item) => item.device_id === numericId
    );
    setDeviceData(filteredData);
    setIsLoading(false);
  }, [numericId]);

  useEffect(() => {
    loadSacDm();
  }, [loadSacDm]);

  useEffect(() => {
    const intervalId = setInterval(() => {
      loadSacDm();
    }, 5000);

    return () => clearInterval(intervalId);
  }, [loadSacDm]);

  return (
    <>
      <h1>Device {id}</h1>
      <Description>
        Visualização detalhada das métricas do dispositivo.
      </Description>
      {isLoading ? (
        <p>Loading...</p>
      ) : (
        <SacDmDevice
          deviceId={numericId}
          deviceData={deviceData}
          isLoading={isLoading}
        />
      )}
    </>
  );
};
