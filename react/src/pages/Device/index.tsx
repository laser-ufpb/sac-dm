import { useParams } from "react-router-dom";
import { useEffect, useState, useCallback } from "react";
import { SacDmProps } from "../SacDm/types";
import { Description } from "./styles";
import { SacDmDevice } from "../SacDm/components/SacDmDevice";
import { formatTime } from "../../utils/formatTime";
import { BackPage } from "../../components/BackPage";
import { AirplanemodeActive } from "@mui/icons-material";
import { DeviceProps } from "../DeviceList/types";
import sacDmService from "../../app/services/sac_dm";
import deviceService from "../../app/services/devices";

export const Device = () => {
  const { id } = useParams();
  const numericId = Number(id);

  const [isLoading, setIsLoading] = useState(true);
  const [sacDm, setSacDm] = useState<SacDmProps[]>([]);
  const [device, setDevice] = useState<DeviceProps>();

  const loadSacDm = useCallback(async () => {
    if (!numericId) return;
    setIsLoading(true);
    try {
      const response = await sacDmService.getSacDm();
      const formattedResponse = response.map((item: SacDmProps) => ({
        ...item,
        timestamp: formatTime(item.timestamp),
      }));
      const filteredData = formattedResponse.filter(
        (item: SacDmProps) => item.device_id === numericId
      );

      if (JSON.stringify(sacDm) !== JSON.stringify(filteredData)) {
        setSacDm(filteredData);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  }, [numericId, sacDm]);

  const loadDevices = useCallback(async () => {
    try {
      const response = await deviceService.getDevices();
      if (response.length > 0) {
        setDevice(
          response.find((device: DeviceProps) => device.id === numericId)
        );
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  }, [numericId]);

  useEffect(() => {
    loadSacDm();
    loadDevices();
  }, [loadSacDm, loadDevices]);

  useEffect(() => {
    const intervalId = setInterval(() => {
      loadSacDm();
    }, 5000);

    return () => clearInterval(intervalId);
  }, [loadSacDm]);

  return (
    <>
      <BackPage />
      {device && (
        <Description>
          <h1>
            <AirplanemodeActive
            // sx={{
            //   color: getStatusColor(device.status_id),
            // }}
            />
            Device {device.device_code}
          </h1>
          <p>Visualização detalhada das métricas do dispositivo.</p>
          <p>
            Última atualização:{" "}
            {sacDm.length > 0 ? sacDm[sacDm.length - 1].timestamp : "N/A"}
          </p>
        </Description>
      )}
      {/* {isLoading ? (
        <p>Loading...</p>
      ) : ( */}
      <SacDmDevice deviceId={numericId} sacDm={sacDm} isLoading={isLoading} />
      {/* )} */}
    </>
  );
};
