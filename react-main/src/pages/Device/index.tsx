// import { useParams } from "react-router-dom";
// import { useEffect, useState, useCallback } from "react";
// import { SacDmProps } from "../SacDm/types";
// import { Description } from "./styles";
// import { SacDmDevice } from "../SacDm/components/SacDmDevice";
// import { formatTime } from "../../utils/formatTime";
// import { BackPage } from "../../components/BackPage";
// import { AirplanemodeActive } from "@mui/icons-material";
// import { DeviceProps } from "../../types";
// import sacDmService from "../../app/services/sac_dm";
// import deviceService from "../../app/services/devices";
// import DataCountSelect from "../../components/DataCountSelect";

export const Device = () => {
  // const { id } = useParams();
  // const numericId = Number(id);
  // const [dataCount, setDataCount] = useState(100);

  // const [sacDm, setSacDm] = useState<SacDmProps[]>([]);
  // const [device, setDevice] = useState<DeviceProps>();

  // const loadSacDm = useCallback(async () => {
  //   if (!numericId) return;
  //   try {
  //     const response = await sacDmService.getSacDmByFilter({
  //       deviceId: numericId,
  //       limit: dataCount,
  //     });
  //     const formattedResponse = response.map((item: SacDmProps) => ({
  //       ...item,
  //       timestamp: formatTime(item.timestamp),
  //     }));

  //     setSacDm(formattedResponse);
  //   } catch (error) {
  //     console.error(error);
  //   }
  // }, [numericId, dataCount]);

  // const loadDevices = useCallback(async () => {
  //   try {
  //     const response = await deviceService.getDevices();
  //     const foundDevice = response.find(
  //       (device: DeviceProps) => device.id === numericId
  //     );
  //     if (foundDevice) {
  //       setDevice(foundDevice);
  //     }
  //   } catch (error) {
  //     console.error(error);
  //   }
  // }, [numericId]);

  // useEffect(() => {
  //   loadSacDm();
  //   loadDevices();
  // }, [loadSacDm, loadDevices]);

  // useEffect(() => {
  //   const intervalId = setInterval(() => {
  //     loadSacDm();
  //   }, 2000);

  //   return () => clearInterval(intervalId);
  // }, [loadSacDm]);

  return (
    <>
      Device
      {/* <BackPage />
      {device && (
        <Description>
          <h1>
            <AirplanemodeActive
            // sx={{
            //   color: getStatusColor(device.status_id),
            // }}
            />
            Device {device.device_code}
          </h1>
          <p>Visualização detalhada das métricas do dispositivo.</p>
          <p>
            Última atualização:{" "}
            {sacDm.length > 0 ? sacDm[sacDm.length - 1].timestamp : "N/A"}
          </p>
        </Description>
      )}

      {/* <DataCountSelect dataCount={dataCount} setDataCount={setDataCount} /> */}
      {/* <SacDmDevice deviceId={numericId} sacDm={sacDm} />  */}
    </>
  );
};
