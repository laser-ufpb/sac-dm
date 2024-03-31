import { useParams } from "react-router-dom";
import { Container } from "./styles";
import { useEffect, useState } from "react";
import { SacDmProps } from "../SacDm/types";
import sacDmService from "../../app/services/sac_dm";
import { CustomTable } from "../../components/CustomTable";

export const Device = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [deviceData, setDeviceData] = useState<SacDmProps[]>([]);

  const { id } = useParams();
  const numericId = Number(id);

  useEffect(() => {
    loadSacDm();
  }, []);

  const loadSacDm = async () => {
    setIsLoading(true);
    try {
      const response = await sacDmService.getSacDm();
      const filteredData = response.filter(
        (item: SacDmProps) => item.device_id === numericId
      );
      setDeviceData(filteredData);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const columns = [
    { id: "id", label: "ID" },
    { id: "device_id", label: "ID do Dispositivo" },
    { id: "value", label: "Valor" },
    { id: "timestamp", label: "Data" },
  ];

  return (
    <Container>
      <h1>Device {id}</h1>
      <CustomTable columns={columns} data={deviceData} isLoading={isLoading} />
    </Container>
  );
};
