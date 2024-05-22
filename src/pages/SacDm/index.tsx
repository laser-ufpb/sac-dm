import { useEffect, useState } from "react";
// import sacDmService from "../../app/services/sac_dm";
import { SacDmProps } from "./types";
import { DeviceProps } from "../DeviceList/types";
// import DeviceService from "../../app/services/devices";
import {
  SelectContainer,
  StyledOptions,
  StyledSelect,
} from "../DeviceList/components/FilterStatus/styles";
import { ArrowDropDown } from "@mui/icons-material";
import { Container } from "./styles";
import mockdevices from "../../mock/devices.json";
import mocksacdm from "../../mock/sacdm.json";
import { SacDmDevice } from "../Device/components/SacDmDevice";
import { formatTime } from "../../utils/formatTime";

export const SacDm = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [sacDm, setSacDm] = useState<SacDmProps[]>([]);
  const [selectedDeviceId, setSelectedDeviceId] = useState(
    mocksacdm[0].device_id
  );
  const [sacDmFiltered, setSacDmFiltered] = useState<SacDmProps[]>([]);
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
    setSacDmFiltered(filteredData);
  }, [selectedDeviceId, sacDm]);

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
      <SacDmDevice
        deviceId={selectedDeviceId}
        sacDm={sacDmFiltered}
        isLoading={isLoading}
      />
    </>
  );
};
