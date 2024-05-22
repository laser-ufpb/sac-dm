import { useParams } from "react-router-dom";
import { useEffect, useState, useCallback } from "react";
import { SacDmProps } from "../SacDm/types";
import { Description } from "./styles";
import { SacDmDevice } from "./components/SacDmDevice";
import mocksacdm from "../../mock/sacdm.json";
import mockdevices from "../../mock/devices.json";
import { formatTime } from "../../utils/formatTime";
import { BackPage } from "../../components/BackPage";
import { AirplanemodeActive } from "@mui/icons-material";
import { getStatusColor } from "../../app/utils/getStatusColor";
import { DeviceProps } from "../DeviceList/types";

export const Device = () => {
  const { id } = useParams();
  const numericId = Number(id);

  const [isLoading, setIsLoading] = useState(true);
  const [sacDm, setSacDm] = useState<SacDmProps[]>([]);
  const [device] = useState<DeviceProps>(
    mockdevices.find((item) => item.id === numericId) as DeviceProps
  );

  const loadSacDm = useCallback(async () => {
    setIsLoading(true);
    const formattedResponse = mocksacdm.map((item: SacDmProps) => ({
      ...item,
      timestamp: formatTime(item.timestamp),
    }));
    const filteredData = formattedResponse.filter(
      (item) => item.device_id === numericId
    );
    setSacDm(filteredData);
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
      <BackPage />
      <Description>
        <h1>
          <AirplanemodeActive
            sx={{
              color: getStatusColor(device.status),
            }}
          />
          Device {device.device_code}
        </h1>
        <p>Visualização detalhada das métricas do dispositivo.</p>
        <p>
          Última atualização:{" "}
          {sacDm.length > 0 ? sacDm[sacDm.length - 1].timestamp : "N/A"}
        </p>
      </Description>
      {isLoading ? (
        <p>Loading...</p>
      ) : (
        <SacDmDevice deviceId={numericId} sacDm={sacDm} isLoading={isLoading} />
      )}
    </>
  );
};
