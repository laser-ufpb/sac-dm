import { useEffect, useState } from "react";
import DeviceService from "../../app/services/devices";
import { DeviceProps } from "./types";
import { Container, Header, TableBox } from "./styles";
import formatDate from "../../app/utils/formatDate";
import { CustomTable } from "../../components/CustomTable";
import { Button } from "@mui/material";
import { AddCircle } from "@mui/icons-material";
import { AddDevice } from "./components/AddDevice";
import { useNavigate } from "react-router-dom";

export const DeviceList = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [devices, setDevices] = useState<DeviceProps[]>([]);
  const [openAddDeviceModal, setOpenAddDeviceModal] = useState(false);

  const navigate = useNavigate();

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

  const handleCellClick = (deviceId: number) => {
    console.log(deviceId);
    navigate(`/device/${deviceId}`);
  };

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
            onCellClick={handleCellClick}
          />
        </TableBox>
      </Container>
    </>
  );
};
