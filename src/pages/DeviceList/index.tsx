import { useEffect, useState } from "react";
import DeviceService from "../../app/services/devices";
import { DeviceProps } from "./types";
import {
  Container,
  DeviceItem,
  DevicesList,
  Header,
  NoDevicesMessage,
} from "./styles";
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

const statusOptions = ["Crítico", "Alerta", "Saudável", "Offline"];

export const DeviceList = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [devices, setDevices] = useState<DeviceProps[]>([]);
  const [openAddDeviceModal, setOpenAddDeviceModal] = useState(false);
  const [filterStatus, setFilterStatus] = useState<string[]>([]);

  const navigate = useNavigate();

  useEffect(() => {
    loadDevices();
  }, []);

  const loadDevices = async () => {
    setIsLoading(true);
    try {
      let response = await DeviceService.getDevices();
      response = response.map((device: DeviceProps) => ({
        ...device,
        status: ["Saudável", "Alerta", "Crítico", "Offline"][
          Math.floor(Math.random() * 4)
        ],
      }));

      const statusPriority = {
        Crítico: 1,
        Alerta: 2,
        Saudável: 3,
        Offline: 4,
      };

      response.sort(
        (a: DeviceProps, b: DeviceProps) =>
          statusPriority[a.status] - statusPriority[b.status]
      );

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

  const filteredDevices = devices.filter((device) =>
    filterStatus.length > 0 ? filterStatus.includes(device.status) : true
  );

  return (
    <>
      <AddDevice
        open={openAddDeviceModal}
        onClose={() => setOpenAddDeviceModal(false)}
        onSubmitted={loadDevices}
      />
      <Container>
        <Header>
          <h2>Lista de Dispositivos</h2>

          <FilterStatus
            statusOptions={statusOptions}
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

        {isLoading && <CircularProgress />}
        {!isLoading && (
          <>
            {filteredDevices.length > 0 ? (
              <DevicesList>
                {filteredDevices.map((device) => (
                  <DeviceItem
                    key={device.id}
                    onClick={() => handleCellClick(device.id)}
                  >
                    {device.status !== "Offline" ? (
                      <AirplanemodeActive
                        sx={{
                          color: getStatusColor(device.status),
                        }}
                      />
                    ) : (
                      <AirplanemodeInactive
                        sx={{
                          color: getStatusColor(device.status),
                        }}
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
        )}
      </Container>
    </>
  );
};
