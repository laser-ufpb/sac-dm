import Chart from "react-apexcharts";
import { SacDmProps } from "../../SacDm/types";
import { EmptyData } from "../../../components/EmptyData";

export const SacDmDevice = ({
  deviceId,
  sacDm,
  isLoading,
}: {
  deviceId: number | null;
  sacDm: SacDmProps[];
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
      categories: sacDm.map((item) => item.timestamp),
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
      data: sacDm.map((item) => item.value),
    },
  ];

  return (
    <div style={{ zIndex: 0 }}>
      {deviceId && !isLoading && sacDm.length > 0 ? (
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
