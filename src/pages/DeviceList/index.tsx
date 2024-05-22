import { useEffect, useState } from "react";
// import DeviceService from "../../app/services/devices";
import { DeviceProps } from "./types";
import { DeviceItem, DevicesList, Header, NoDevicesMessage } from "./styles";
import { Button, CircularProgress } from "@mui/material";
import {
  AddCircle,
  AirplanemodeActive,
  AirplanemodeInactive,
} from "@mui/icons-material";
import { AddDevice } from "./components/AddDevice";
import { useNavigate } from "react-router-dom";
import { getStatusColor } from "../../app/utils/getStatusColor";
import { FilterStatus } from "./components/FilterStatus";
import deviceService from "../../app/services/devices";

export const DeviceList = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [devices, setDevices] = useState<DeviceProps[]>([]);
  const [openAddDeviceModal, setOpenAddDeviceModal] = useState(false);
  const [filterStatus, setFilterStatus] = useState<number[]>([]);

  const navigate = useNavigate();

  useEffect(() => {
    loadDevices();
  }, []);

  const loadDevices = async () => {
    setIsLoading(true);
    try {
      let response = await deviceService.getDevices();
      response = response.map((device: DeviceProps) => ({
        id: device.id,
        device_code: device.device_code,
        status_id: device.status_id
      }));

      // const statusPriority = {
      //   Crítico: 1,
      //   Alerta: 2,
      //   Saudável: 3,
      //   Offline: 4,
      // };

      // response.sort(
      //   (a: DeviceProps, b: DeviceProps) =>
      //     statusPriority[a.status] - statusPriority[b.status]
      // );

      setDevices(response);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCellClick = (deviceId: number) => {
    navigate(`/device/${deviceId}`);
  };

  const filteredDevices = devices.filter((device) => {
    console.log(device.status_id, filterStatus)

    return (
      filterStatus.length > 0 ? filterStatus.includes(device.status_id) : true
    )
  }
  );

  return (
    <>
      <AddDevice
        open={openAddDeviceModal}
        onClose={() => setOpenAddDeviceModal(false)}
        onSubmitted={loadDevices}
      />
      <Header>
        <h2>Lista de Dispositivos</h2>

        <FilterStatus
          filterStatus={filterStatus}
          setFilterStatus={setFilterStatus}
        />

        <Button
          variant="contained"
          startIcon={<AddCircle />}
          onClick={() => setOpenAddDeviceModal(true)}
        >
          <p>Novo Dispositivo</p>
        </Button>
      </Header>

      {isLoading ? (
        <CircularProgress />
      ) : filteredDevices.length > 0 ? (
        <DevicesList>
          {filteredDevices.map((device) => (
            <DeviceItem
              key={device.id}
              onClick={() => handleCellClick(device.id)}
            >
              {device.status_id === 4 ? (
                <AirplanemodeActive
                  sx={{ color: getStatusColor("Offline") }}
                />
              ) : (
                <AirplanemodeInactive
                  sx={{ color: getStatusColor("a") }}
                />
              )}
              <h3>{device.device_code}</h3>
            </DeviceItem>
          ))}
        </DevicesList>
      ) : (
        <NoDevicesMessage>Nenhum dispositivo encontrado</NoDevicesMessage>
      )}
    </>
  );
};
