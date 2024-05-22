import { useParams } from "react-router-dom";
import { useEffect, useState, useCallback } from "react";
import { SacDmProps } from "../SacDm/types";
import { Description } from "./styles";
import { SacDmDevice } from "./components/SacDmDevice";
import mocksacdm from "../../mock/sacdm.json";
import { formatTime } from "../../utils/formatTime";
import { BackPage } from "../../components/BackPage";
import { AirplanemodeActive } from "@mui/icons-material";

export const Device = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [sacDm, setSacDm] = useState<SacDmProps[]>([]);

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
          <AirplanemodeActive />
          Device {id}
        </h1>
        <p>Visualização detalhada das métricas do dispositivo.</p>
      </Description>
      {isLoading ? (
        <p>Loading...</p>
      ) : (
        <SacDmDevice deviceId={numericId} sacDm={sacDm} isLoading={isLoading} />
      )}
    </>
  );
};
