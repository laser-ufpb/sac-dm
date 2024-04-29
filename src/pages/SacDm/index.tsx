import { useEffect, useState } from "react";
import sacDmService from "../../app/services/sac_dm";
import { SacDmProps } from "./types";
import { CustomTable } from "../../components/CustomTable";

export const SacDm = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [sacDm, setSacDm] = useState<SacDmProps[]>([]);

  useEffect(() => {
    loadSacDm();
  }, []);

  const loadSacDm = async () => {
    setIsLoading(true);
    try {
      const response = await sacDmService.getSacDm();
      setSacDm(response);
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
    <>
      <h1>SacDm</h1>
      <CustomTable columns={columns} data={sacDm} isLoading={isLoading} />
    </>
  );
};
