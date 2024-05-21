import { useEffect, useState } from "react";
// import sacDmService from "../../app/services/sac_dm";
import { SacDmProps } from "./types";
import Chart from "react-apexcharts";
import { Checkbox } from "@mui/material";
import { DeviceProps } from "../DeviceList/types";
// import DeviceService from "../../app/services/devices";
import {
  SelectContainer,
  StyledOptions,
  StyledSelect,
} from "../DeviceList/components/FilterStatus/styles";
import { ArrowDropDown, CheckBox } from "@mui/icons-material";
import { Container } from "./styles";
import { EmptyData } from "../../components/EmptyData";
import mockdevices from "../../mock/devices.json";
import mocksacdm from "../../mock/sacdm.json";

const formatTime = (dateString: string) => {
  const date = new Date(dateString);
  return `${date.getDate().toString().padStart(2, "0")}/${(date.getMonth() + 1)
    .toString()
    .padStart(2, "0")}/${date.getFullYear().toString().slice(-2)} às ${date
    .getHours()
    .toString()
    .padStart(2, "0")}:${date.getMinutes().toString().padStart(2, "0")}`;
};

export const SacDm = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [sacDm, setSacDm] = useState<SacDmProps[]>([]);
  const [selectedDeviceId, setSelectedDeviceId] = useState(
    mocksacdm[0].device_id
  );
  const [deviceData, setDeviceData] = useState<SacDmProps[]>([]);
  const [devices, setDevices] = useState<DeviceProps[]>([]);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    loadDevices();
    loadSacDm();
  }, []);

  useEffect(() => {
    const intervalId = setInterval(() => {
      loadSacDm();
      loadDevices();
    }, 5000);

    return () => clearInterval(intervalId);
  }, []);

  const loadDevices = async () => {
    setIsLoading(true);
    setDevices(mockdevices as DeviceProps[]);
    setIsLoading(false);

    // try {
    //   const response = await DeviceService.getDevices();
    //   setDevices(response);
    //   if (response.length > 0) {
    //     setSelectedDeviceId(response[0].id);
    //   }
    // } catch (error) {
    //   console.error(error);
    // } finally {
    //   setIsLoading(false);
    // }
  };

  const loadSacDm = async () => {
    setIsLoading(true);
    const formattedResponse = mocksacdm.map((item: SacDmProps) => ({
      ...item,
      timestamp: formatTime(item.timestamp),
    }));
    setSacDm(formattedResponse);
    setIsLoading(false);
    // try {
    //   const response = await sacDmService.getSacDm();
    //   const formattedResponse = response.map((item: SacDmProps) => ({
    //     ...item,
    //     timestamp: formatTime(item.timestamp),
    //   }));
    //   setSacDm(formattedResponse);
    // } catch (error) {
    //   console.error(error);
    // } finally {
    //   setIsLoading(false);
    // }
  };

  useEffect(() => {
    const filteredData = sacDm.filter(
      (item) => item.device_id === selectedDeviceId
    );
    setDeviceData(filteredData);
  }, [selectedDeviceId, sacDm]);

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

  const handleChange = (deviceId: number, isChecked: boolean) => {
    if (isChecked && deviceId !== selectedDeviceId) {
      setSelectedDeviceId(deviceId);
    }
    setOpen(false);
  };

  return (
    <>
      <Container>
        <SelectContainer>
          <StyledSelect
            onClick={() => setOpen(!open)}
            style={{ borderRadius: open ? "8px 8px 0 0" : "8px" }}
          >
            <CheckBox />
            {
              devices.find((device) => device.id === selectedDeviceId)
                ?.device_code
            }
            <ArrowDropDown />
          </StyledSelect>

          {open && (
            <StyledOptions>
              {devices.map((device: DeviceProps) => (
                <div key={device.id}>
                  <Checkbox
                    color="primary"
                    checked={device.id === selectedDeviceId}
                    onChange={(e) => handleChange(device.id, e.target.checked)}
                  />
                  {device.device_code}
                </div>
              ))}
            </StyledOptions>
          )}
        </SelectContainer>
      </Container>
      <div style={{ zIndex: 0 }}>
        {selectedDeviceId && !isLoading && deviceData.length > 0 ? (
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
    </>
  );
};
