import { useEffect, useState } from "react";
import DeviceService from "../../app/services/devices";
import { DeviceProps } from "./types";
import { Container, Header, TableBox } from "./styles";
import formatDate from "../../app/utils/formatDate";
import { CustomTable } from "../../components/CustomTable";
import { Button } from "@mui/material";
import { AddCircle } from "@mui/icons-material";
import { AddDevice } from "./components/AddDevice";

export const Devices = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [devices, setDevices] = useState<DeviceProps[]>([]);
  const [openAddDeviceModal, setOpenAddDeviceModal] = useState(false);

  useEffect(() => {
    loadDevices();
  }, []);

  const loadDevices = async () => {
    setIsLoading(true);
    try {
      const response = await DeviceService.getDevices();
      setDevices(response);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const columns = [
    { id: "id", label: "ID" },
    { id: "device_code", label: "Código do Dispositivo" },
    { id: "timestamp", label: "Última Atualização", format: formatDate },
  ];

  const formattedData = devices.map((device) => ({
    ...device,
    timestamp: formatDate(device.timestamp),
  }));

  return (
    <>
      <AddDevice
        open={openAddDeviceModal}
        onClose={() => setOpenAddDeviceModal(false)}
        onSubmitted={loadDevices}
      />
      <Container>
        <Header>
          <h1>Dispositivos</h1>
          <Button
            variant="contained"
            startIcon={<AddCircle />}
            onClick={() => setOpenAddDeviceModal(true)}
          >
            <p>Novo Dispositivo</p>
          </Button>
        </Header>
        <TableBox>
          <CustomTable
            columns={columns}
            data={formattedData}
            isLoading={isLoading}
          />
        </TableBox>
      </Container>
    </>
  );
};
