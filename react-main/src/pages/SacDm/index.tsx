import { useCallback, useEffect, useState } from "react";
import { SacDmProps } from "./types";
import { DeviceProps } from "../../types";
import { Container } from "./styles";
import deviceService from "../../app/services/devices";
import sacDmService from "../../app/services/sac_dm";
import SacDmDevice from "./components/SacDmDevice";
import { formatTime } from "../../utils/formatTime";
import DataCountSelect from "../../components/DataCountSelect";
import { CustomSelect } from "../../components/CustomSelect";

export const SacDm = () => {
  const [sacDm, setSacDm] = useState<SacDmProps[]>([]);
  const [selectedDeviceId, setSelectedDeviceId] = useState<number | null>(1);
  const [devices, setDevices] = useState<DeviceProps[]>([]);
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
    if (selectedDeviceId === null) return;
    try {
      const response = await sacDmService.getSacDmByFilter({
        deviceId: selectedDeviceId,
        limit: dataCount,
      });
      const formattedResponse = response.map((item: SacDmProps) => ({
        ...item,
        timestamp: formatTime(item.timestamp),
      }));

      if (JSON.stringify(sacDm) !== JSON.stringify(formattedResponse)) {
        setSacDm(formattedResponse);
      }
    } catch (error) {
      console.error(error);
    }
  }, [selectedDeviceId, dataCount, sacDm]);

  useEffect(() => {
    loadDevices();
    loadSacDm();
  }, [loadDevices, loadSacDm]);

  useEffect(() => {
    const intervalId = setInterval(() => {
      loadSacDm();
    }, 2000);

    return () => clearInterval(intervalId);
  }, [loadSacDm]);

  return (
    <>
      <Container>
        <CustomSelect
          label="Selecionar Dispositivo"
          options={devices.map((device) => ({
            id: device.id,
            description: device.device_code,
          }))}
          selectedOption={selectedDeviceId}
          setSelectedOption={setSelectedDeviceId}
        />
      </Container>

      <DataCountSelect dataCount={dataCount} setDataCount={setDataCount} />
      {selectedDeviceId && (
        <SacDmDevice
          key={selectedDeviceId}
          deviceId={selectedDeviceId}
          sacDm={sacDm}
        />
      )}
    </>
  );
};
