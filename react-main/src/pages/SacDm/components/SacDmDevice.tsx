import Chart from "react-apexcharts";
import { SacDmProps } from "../../SacDm/types";
import { EmptyData } from "../../../components/EmptyData";
import React, { useCallback, useEffect, useState } from "react";
import { SacDmDefaultProps } from "../../../types";
import sacDmDefault from "../../../app/services/sacdm_default";
import { Divider, Section, containerStyle, statusBoxStyle, statusOkStyle, statusFailStyle, checklistContainerStyle, checklistItemStyle, checklistCircleStyle, chartContainerStyle } from "../styles";

export const SacDmDevice = ({
  deviceId,
  sacDm,
}: {
  deviceId: number;
  sacDm: SacDmProps[];
}) => {
  const [sacDmMean, setsacDmMean] = useState<SacDmDefaultProps>();
  //const [problemStatus, setProblemStatus] = useState<"OK" | "Falha">("OK");

const loadSacDmDefault = useCallback(async () => {
  try {
    const response = await sacDmDefault.getSacDmDefault(deviceId);
    setsacDmMean(response);
  } catch (error) {
    console.error(error);
  }
}, [deviceId]);

useEffect(() => {
  loadSacDmDefault();

  const dataInterval = setInterval(() => {
    loadSacDmDefault();
  }, 5000);

  // const statusInterval = setInterval(() => {
  //   setProblemStatus((prevStatus) => (prevStatus === "OK" ? "Falha" : "OK"));
  // }, 5000);

  return () => {
    clearInterval(dataInterval);
    //clearInterval(statusInterval);
  };
}, [loadSacDmDefault]);

if (!deviceId) {
  return null;
}

// Hardcoded[WiP]
const checkDataStatus = () => {
  return "OK"
  // return problemStatus;
};

// Hardcoded[WiP]
const checkProblemStatus = () => {
  return "OK"
  // return problemStatus;
};

  

  const calculateDynamicLimits = (data: number[], mean: number, stdDev: number) => {
    const margin = stdDev * 0.5; // Espaço adicional baseado no desvio padrão
    return {
      min: mean - 3 * stdDev - margin,
      max: mean + 3 * stdDev + margin,
    };
  };

  const getChartData = (axis: "x" | "y" | "z") => {
    const values = sacDm.map((item) => parseFloat(item[`${axis}_value`].toFixed(8)));
    const means = Array(sacDm.length).fill(sacDmMean?.[`${axis}_mean`] ?? 0);
    const upperStandardDeviation = sacDmMean
      ? Array(sacDm.length).fill(
          sacDmMean[`${axis}_mean`] + sacDmMean[`${axis}_standard_deviation`]
        )
      : [];
    const lowerStandardDeviation = sacDmMean
      ? Array(sacDm.length).fill(
          sacDmMean[`${axis}_mean`] - sacDmMean[`${axis}_standard_deviation`]
        )
      : [];

    return {
      series: [
        { name: "Valor", data: values },
        { name: "Média", data: means },
        { name: "Desvio Padrão Superior", data: upperStandardDeviation },
        { name: "Desvio Padrão Inferior", data: lowerStandardDeviation },
      ],
      limits: calculateDynamicLimits(
        values,
        sacDmMean?.[`${axis}_mean`] ?? 0,
        sacDmMean?.[`${axis}_standard_deviation`] ?? 0
      ),
    };
  };

  const dataX = getChartData("x");
  const dataY = getChartData("y");
  const dataZ = getChartData("z");
  const status = checkDataStatus() === "OK" ? statusOkStyle : statusFailStyle;

  const createOptionsChart = (limits: { min: number; max: number }) => {
    // Função para formatar valores em notação científica com expoente sobrescrito
    const formatScientific = (num: number): string => {
      const superscripts = ["⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"];
      const [coefficient, exponent] = num
        .toExponential(2)
        .split("e")
        .map((part, index) => (index === 1 ? parseInt(part) : parseFloat(part)));
  
      // Substituir números do expoente por seus equivalentes em Unicode
      const formattedExponent = exponent
        .toString()
        .split("")
        .map((char) => (char === "-" ? "⁻" : superscripts[parseInt(char)]))
        .join("");
  
      return `${coefficient.toString().replace(".", ",")} × 10${formattedExponent}`;
    };
  
    return {
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
        min: limits.min,
        max: limits.max,
        labels: {
          formatter: (value: number) =>
            value ? formatScientific(value) : "0,00 × 10⁰",
          style: {
            colors: ["#E0E0E0"],
          },
        },
      },
      tooltip: {
        theme: "dark",
        y: {
          formatter: (value: number) =>
            value ? formatScientific(value) : "0,00 × 10⁰",
        },
        fixed: {
          enabled: false,
        },
      },
      legend: {
        labels: {
          colors: ["#E0E0E0", "#E0E0E0", "#E0E0E0", "#E0E0E0"],
        },
      },
    };
  };
  
  

  return (
    <div style={containerStyle}>
      <div style={{ ...statusBoxStyle, ...status }}>{checkDataStatus()}</div>
      <div style={checklistContainerStyle}>
        {["Item 1", "Item 2", "Item 3", "Item 4"].map((item, index) => {
          const hasError = checkProblemStatus() === "Falha"; // Condição para erro
          return (
            <div key={index} style={checklistItemStyle}>
              <div style={checklistCircleStyle(hasError)}></div>
              <span>{item}</span>
            </div>
          );
        })}
      </div>

      <div
  style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: "16px", }}
>
  {[
    { title: "Eixo X", data: dataX },
    { title: "Eixo Y", data: dataY },
    { title: "Eixo Z", data: dataZ },
  ].map(({ title, data }, index) => (
    <Section key={index} style={chartContainerStyle}>
      <h3>{title}</h3>
      <Chart
        options={createOptionsChart(data.limits)}
        series={data.series}
        type="line"
        height="300"
        width="100%"
      />
    </Section>
  ))}
</div>

{sacDm.length === 0 && (
  <EmptyData message="Nenhum dado encontrado para o dispositivo selecionado" />
)}
    </div>
  );
};

export default SacDmDevice;
