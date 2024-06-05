import Chart from "react-apexcharts";
import { SacDmProps } from "../../SacDm/types";
import { EmptyData } from "../../../components/EmptyData";

export const SacDmDevice = ({
  deviceId,
  sacDm,
}: {
  deviceId: number | null;
  sacDm: SacDmProps[];
}) => {
  if (!deviceId) {
    return null;
  }

  // Calcular média e desvio padrão
  const values = sacDm.map((item: SacDmProps) => +item.value.toFixed(8));
  const mean = values.reduce((acc, value) => acc + value, 0) / values.length;
  const stdDev = Math.sqrt(
    values.reduce((acc, value) => acc + (value - mean) ** 2, 0) / values.length
  );

  // Criar séries para média e desvio padrão
  const meanSeries = Array(values.length).fill(mean);
  const stdDevUpper = meanSeries.map((m) => m + stdDev);
  const stdDevLower = meanSeries.map((m) => m - stdDev);

  const optionsChart = {
    chart: {
      id: "device-metrics",
    },
    xaxis: {
      categories: sacDm.map((item: SacDmProps) => item.timestamp),
      labels: {
        show: false,
      },
    },
    yaxis: {
      labels: {
        formatter: (value: number) => value.toFixed(8), // Formatando labels do eixo y para mostrar 8 casas decimais
      },
    },
    tooltip: {
      theme: "dark",
      y: {
        formatter: (value: number) => value.toFixed(8), // Formatando valores do tooltip para mostrar 8 casas decimais
      },
    },
  };

  const seriesChart = [
    {
      name: "Valor",
      data: values,
    },
    {
      name: "Média",
      data: meanSeries.map((value) => parseFloat(value.toFixed(8))), // Garantindo a precisão de 8 casas decimais
    },
    {
      name: "Desvio Padrão Superior",
      data: stdDevUpper.map((value) => parseFloat(value.toFixed(8))),
    },
    {
      name: "Desvio Padrão Inferior",
      data: stdDevLower.map((value) => parseFloat(value.toFixed(8))),
    },
  ];

  return (
    <div style={{ zIndex: 0, position: "relative" }}>
      <Chart
        options={optionsChart}
        series={seriesChart}
        type="line"
        height="350"
      />
      {sacDm.length === 0 && (
        <EmptyData message="Nenhum dado encontrado para o dispositivo selecionado" />
      )}
    </div>
  );
};
