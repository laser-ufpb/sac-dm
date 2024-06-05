import { useCallback, useEffect, useState } from "react";
import { SacDmProps } from "./types";
import { DeviceProps } from "../DeviceList/types";
import {
  SelectContainer,
  StyledOptions,
  StyledSelect,
} from "../DeviceList/components/FilterStatus/styles";
import { ArrowDropDown } from "@mui/icons-material";
import { Container } from "./styles";
import deviceService from "../../app/services/devices";
import sacDmService from "../../app/services/sac_dm";
import { SacDmDevice } from "./components/SacDmDevice";
import { formatTime } from "../../utils/formatTime";
import DataCountSelect from "../../components/DataCountSelect";

export const SacDm = () => {
  const [sacDm, setSacDm] = useState<SacDmProps[]>([]);
  const [selectedDeviceId, setSelectedDeviceId] = useState(1);
  const [devices, setDevices] = useState<DeviceProps[]>([]);
  const [open, setOpen] = useState(false);
  const [dataCount, setDataCount] = useState(100);

  const loadDevices = useCallback(async () => {
    try {
      const response = await deviceService.getDevices();
      setDevices(response);
      const deviceIds = response.map((device: DeviceProps) => device.id);
      if (!deviceIds.includes(selectedDeviceId) && response.length > 0) {
        setSelectedDeviceId(response[0].id);
      }
    } catch (error) {
      console.error(error);
    }
  }, [selectedDeviceId]);

  const loadSacDm = useCallback(async () => {
    if (!selectedDeviceId) return;
    try {
      const response = await sacDmService.getSacDmByFilter({
        deviceId: selectedDeviceId,
        limit: dataCount,
      });
      const formattedResponse = response.map((item: SacDmProps) => ({
        ...item,
        timestamp: formatTime(item.timestamp),
      }));
      setSacDm(formattedResponse);
    } catch (error) {
      console.error(error);
    }
  }, [selectedDeviceId, dataCount]);

  useEffect(() => {
    loadDevices();
    loadSacDm();
  }, [loadDevices, loadSacDm]);

  useEffect(() => {
    const intervalId = setInterval(() => {
      loadSacDm();
      loadDevices();
    }, 2000);

    return () => clearInterval(intervalId);
  }, [loadSacDm, loadDevices]);

  const handleSelectDevice = (deviceId: number) => {
    setSelectedDeviceId(deviceId);
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
            {
              devices.find((device) => device.id === selectedDeviceId)
                ?.device_code
            }
            <ArrowDropDown />
          </StyledSelect>

          {open && (
            <StyledOptions>
              {devices.map((device: DeviceProps) => (
                <div
                  key={device.id}
                  onClick={() => handleSelectDevice(device.id)}
                  style={{ cursor: "pointer" }}
                >
                  {device.device_code}
                </div>
              ))}
            </StyledOptions>
          )}
        </SelectContainer>
      </Container>

      {/* <DataCountSelect dataCount={dataCount} setDataCount={setDataCount} /> */}
      <SacDmDevice deviceId={selectedDeviceId} sacDm={sacDm} />
    </>
  );
};
