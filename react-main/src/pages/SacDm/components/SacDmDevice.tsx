import Chart from "react-apexcharts";
import { SacDmProps } from "../../SacDm/types";
import { EmptyData } from "../../../components/EmptyData";
import React, { useCallback, useEffect, useState } from "react";
import { SacDmDefaultProps } from "../../../types";
import sacDmDefault from "../../../app/services/sacdm_default";

export const SacDmDevice = ({
  deviceId,
  sacDm,
}: {
  deviceId: number | null;
  sacDm: SacDmProps[];
}) => {
  const [sacDmMean, setsacDmMean] = useState<SacDmDefaultProps>();

  const loadSacDmDefault = useCallback(async () => {
    try {
      const response = await sacDmDefault.getSacDmDefault(1);
      // TODO: Alterar para pegar o veículo selecionado
      setsacDmMean(response);
    } catch (error) {
      console.error(error);
    }
  }, []);

  useEffect(() => {
    loadSacDmDefault();
  }, [loadSacDmDefault]);

  if (!deviceId) {
    return null;
  }

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
        formatter: (value: number) => (value ? value.toFixed(8) : "0.00000000"),
        style: {
          colors: ["#E0E0E0"],
        },
      },
    },
    tooltip: {
      theme: "dark",
      y: {
        formatter: (value: number) => (value ? value.toFixed(8) : "0.00000000"),
      },
    },
    legend: {
      labels: {
        colors: ["E0E0E0", "E0E0E0", "E0E0E0", "E0E0E0"],
      },
    },
  };

  const seriesChart = [
    {
      name: "Valor",
      data: sacDm.map((item) => parseFloat(item.value.toFixed(8))),
    },
    {
      name: "Média",
      data: Array(sacDm.length).fill(sacDmMean?.x_mean),
    },
    {
      name: "Desvio Padrão Superior",
      data: sacDmMean
        ? Array(sacDm.length).fill(
            sacDmMean.x_mean + sacDmMean.x_standard_deviation
          )
        : [],
    },
    {
      name: "Desvio Padrão Inferior",
      data: sacDmMean
        ? Array(sacDm.length).fill(
            sacDmMean.x_mean - sacDmMean.x_standard_deviation
          )
        : [],
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

export default React.memo(SacDmDevice, (prevProps, nextProps) => {
  return (
    prevProps.deviceId === nextProps.deviceId &&
    JSON.stringify(prevProps.sacDm) === JSON.stringify(nextProps.sacDm)
  );
});
