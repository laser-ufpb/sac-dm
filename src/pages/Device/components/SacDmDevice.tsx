import Chart from "react-apexcharts";
import { SacDmProps } from "../../SacDm/types";
import { EmptyData } from "../../../components/EmptyData";

export const SacDmDevice = ({
  deviceId,
  deviceData,
  isLoading,
}: {
  deviceId: number | null;
  deviceData: SacDmProps[];
  isLoading: boolean;
}) => {
  if (!deviceId) {
    return null;
  }

  const optionsChart = {
    chart: {
      id: "device-metrics",
    },
    xaxis: {
      categories: deviceData.map((item) => item.timestamp),
      labels: {
        show: false,
      },
    },
    tooltip: {
      theme: "dark",
    },
  };

  const seriesChart = [
    {
      name: "Valor",
      data: deviceData.map((item) => item.value),
    },
  ];

  return (
    <div style={{ zIndex: 0 }}>
      {deviceId && !isLoading && deviceData.length > 0 ? (
        <Chart
          options={optionsChart}
          series={seriesChart}
          type="line"
          height={350}
        />
      ) : (
        <EmptyData message="Nenhum dado encontrado para o dispositivo selecionado" />
      )}
    </div>
  );
};
