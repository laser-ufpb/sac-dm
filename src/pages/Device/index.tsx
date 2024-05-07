import { useParams } from "react-router-dom";
import { useCallback, useEffect, useState } from "react";
import { SacDmProps } from "../SacDm/types";
import sacDmService from "../../app/services/sac_dm";
import Chart from "react-apexcharts";
import { theme } from "../../styles/theme";
import { Description } from "./styles";

export const Device = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [deviceData, setDeviceData] = useState<SacDmProps[]>([]);

  const { id } = useParams();
  const numericId = Number(id);

  const loadSacDm = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await sacDmService.getSacDm();
      const filteredData = response
        .filter((item: SacDmProps) => item.device_id === numericId)
        .map((item: SacDmProps) => ({
          ...item,
          timestamp: formatDate(item.timestamp),
        }));
      setDeviceData(filteredData);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  }, [numericId]);

  useEffect(() => {
    loadSacDm();
  }, [loadSacDm]);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const day = String(date.getDate()).padStart(2, "0");
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");

    return `${day}/${month}/${year} ${hours}:${minutes}`;
  };

  const optionsChart: ApexCharts.ApexOptions = {
    chart: {
      id: "basic-bar",
    },
    xaxis: {
      categories: deviceData.map((item) => item.timestamp),
      labels: {
        style: {
          colors: theme.text,
        },
        rotate: -45,
        rotateAlways: true,
      },
    },
    tooltip: {
      theme: "dark",
    },
  };

  const seriesChart: ApexCharts.ApexOptions["series"] = [
    {
      name: "Valor",
      data: deviceData.map((item) => item.value),
    },
  ];

  return (
    <>
      <h1>Device {id}</h1>
      <Description>
        Visualização detalhada das métricas do dispositivo.
      </Description>
      {isLoading ? (
        <p>Loading...</p>
      ) : (
        <Chart options={optionsChart} series={seriesChart} type="line" />
      )}
    </>
  );
};
