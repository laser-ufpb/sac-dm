import { useEffect, useState } from "react";
import sacDmService from "../../app/services/sac_dm";
import { SacDmProps } from "./types";
import Chart from "react-apexcharts";
import { Checkbox } from "@mui/material";
import { DeviceProps } from "../DeviceList/types";
import DeviceService from "../../app/services/devices";
import {
  SelectContainer,
  StyledOptions,
  StyledSelect,
} from "../DeviceList/components/FilterStatus/styles";
import { ArrowDropDown } from "@mui/icons-material";
import { Container } from "./styles";

const formatTime = (dateString: string) => {
  const date = new Date(dateString);
  return `${date.getHours().toString().padStart(2, "0")}:${date
    .getMinutes()
    .toString()
    .padStart(2, "0")}:${date.getSeconds().toString().padStart(2, "0")}`;
};

export const SacDm = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [sacDm, setSacDm] = useState<SacDmProps[]>([]);
  const [selectedDeviceId, setSelectedDeviceId] = useState(0);
  const [deviceData, setDeviceData] = useState<SacDmProps[]>([]);
  const [devices, setDevices] = useState<DeviceProps[]>([]);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    loadSacDm();
    loadDevices();
  }, []);

  const loadDevices = async () => {
    setIsLoading(true);
    try {
      const response = await DeviceService.getDevices();
      setDevices(response);
      setSelectedDeviceId(response[0].id);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadSacDm = async () => {
    setIsLoading(true);
    try {
      const response = await sacDmService.getSacDm();
      const formattedResponse = response.map((item: SacDmProps) => ({
        ...item,
        timestamp: formatTime(item.timestamp),
      }));
      setSacDm(formattedResponse);
      if (formattedResponse.length > 0 && !selectedDeviceId) {
        setSelectedDeviceId(formattedResponse[0].device_id.toString());
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (selectedDeviceId) {
      const filteredData = sacDm.filter(
        (item) => item.device_id === selectedDeviceId
      );
      setDeviceData(filteredData);
    }
  }, [selectedDeviceId, sacDm]);

  const optionsChart = {
    chart: {
      id: "device-metrics",
    },
    xaxis: {
      categories: deviceData.map((item) => item.timestamp),
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
    if (isChecked) {
      setSelectedDeviceId(deviceId);
      loadSacDm();
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
            Filtrar
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
        {selectedDeviceId && !isLoading && (
          <Chart
            options={optionsChart}
            series={seriesChart}
            type="line"
            height={350}
          />
        )}
      </div>
    </>
  );
};
