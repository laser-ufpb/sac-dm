import Chart from "react-apexcharts";
import { SacDmProps } from "../../SacDm/types";
import { EmptyData } from "../../../components/EmptyData";
import React, { useCallback, useEffect, useState } from "react";
import { SacDmDefaultProps } from "../../../types";
import sacDmDefault from "../../../app/services/sacdm_default";
import logsVehicle from "../../../app/services/logs";
import conditionService from "../../../app/services/condition";
import sacDmService from "../../../app/services/sac_dm";
import { Divider, Section, containerStyle, statusBoxStyle, statusOkStyle, statusFailStyle, logContainerStyle, logItemStyle, checklistContainerStyle, checklistItemStyle, checklistCircleStyle, chartContainerStyle } from "../styles";
import {LogsVehicle} from "./Log_vehicles";
import vehicleService from "../../../app/services/vehicle";

export const SacDmDevice = ({
  vehicleId,
  sacDm,
}: {
  vehicleId: number;
  sacDm: SacDmProps[];
}) => {
  const [sacDmMean, setsacDmMean] = useState<SacDmDefaultProps>();
  //const [problemStatus, setProblemStatus] = useState<"OK" | "Falha">("OK");
  const [conditions, setConditions] = useState<{ id: number; description: string }[]>([]);
  const [newStatus, setStatus] = useState<string>();
  const [logs, setLogs] = useState<string[]>([]);
  const [isLogsModalOpen, setLogsModalOpen] = useState(false);

  const handleOpenLogModal = () => setLogsModalOpen(true);
  const handleCloseLogModal = () => setLogsModalOpen(false);


const loadSacDmDefault = useCallback(async () => {
  try {
    const response = await sacDmDefault.getSacDmDefault(vehicleId);
    setsacDmMean(response);
  } catch (error) {
    console.error(error);
  }
}, [vehicleId]);

const fetchConditions = useCallback(async () => {
  try {
    const response = await conditionService.getConditions()
    setConditions(response);
    
    //setLogs(response);
  } catch (error) {
    console.error("Erro ao buscar condições", error);
  }
}, []);

const fetchLogs = useCallback(async () => {
  try {
    const response = await logsVehicle.getLogs(vehicleId);

    // Substituir condition_id pela description correspondente
    const formattedLogs = response.map((log: any) => {
      const condition = conditions.find(c => c.id === log.condition_id);
      const sac = sacDm.find(sac => sac.id === log.sacdm_id);

      // Converter timestamp para objeto Date
      const dateObj = new Date(log.timestamp);

      const formattedDate = dateObj.toLocaleDateString("pt-BR", {
        day: "2-digit",
        month: "short",
        year: "numeric",
      }).replace(".", "");

      const formattedTime = dateObj.toLocaleTimeString("pt-BR", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      });

      const colorCondition = condition?.description === "falha"? "#F44336": "#4CAF50"
      return <>
      <span style={{color: colorCondition }}>
      [{condition?.description || "Desconhecido"}]
      </span>
      {" - "}
      <span style={{ color: "#1E88E5" }}>
      Data: {formattedDate} - Hora: {formattedTime}
      </span>
      <br />
      SACDM: {sac ? `x: ${sac.x_value}, y: ${sac.y_value}, z: ${sac.z_value}, label: ${sac.label}` : "Desconhecido"}
    </>
    }).reverse();
    setLogs(formattedLogs);
    
    //setLogs(response);
  } catch (error) {
    console.error("Erro ao buscar logs", error);
  }
}, [vehicleId,conditions]);

const checkDataStatus = useCallback(async () => {
  try {
    const response = await vehicleService.getVehicleById(vehicleId);
    const condition = conditions.find(c => c.id === response.condition_id);

    setStatus(condition?.description);
  } catch (error) {
    console.error(error);
  }
}, [vehicleId,conditions]);

useEffect(() => {
  loadSacDmDefault();
  fetchConditions();
  fetchLogs();
  checkDataStatus();

  const dataInterval = setInterval(() => {
    loadSacDmDefault();
    fetchLogs();
    checkDataStatus();
  }, 5000);

  // const statusInterval = setInterval(() => {
  //   setProblemStatus((prevStatus) => (prevStatus === "OK" ? "Falha" : "OK"));
  // }, 5000);

  return () => {
    clearInterval(dataInterval);
    //clearInterval(statusInterval);
  };
}, [loadSacDmDefault,fetchLogs,checkDataStatus]);

if (!vehicleId) {
  return null;
}

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
  const status = newStatus === "falha" ? statusFailStyle : statusOkStyle;

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
      <div style={{ ...statusBoxStyle, ...status }}>{status === statusFailStyle ? "Falha" : "Ok"}</div>
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

      <div style={logContainerStyle} onClick={handleOpenLogModal}>
        {logs.slice(0, 3).map((log, index) => (
      <div key={index} style={logItemStyle}>{log}</div>
      ))}
      </div>

      <LogsVehicle open={isLogsModalOpen} onClose={handleCloseLogModal} logs={logs} />

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
