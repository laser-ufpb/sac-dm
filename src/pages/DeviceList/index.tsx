import { useEffect, useState } from "react";
import DeviceService from "../../app/services/devices";
import { DeviceProps } from "./types";
import { Container, DeviceItem, DevicesList, Header } from "./styles";
import {
  Button,
  Checkbox,
  CircularProgress,
  FormControl,
  InputLabel,
  MenuItem,
  OutlinedInput,
  Select,
} from "@mui/material";
import {
  AddCircle,
  AirplanemodeActive,
  AirplanemodeInactive,
} from "@mui/icons-material";
import { AddDevice } from "./components/AddDevice";
import { useNavigate } from "react-router-dom";
import { getStatusColor } from "../../app/utils/getStatusColor";

const statusOptions = ["HEALTHY", "WARNING", "CRITICAL", "OFFLINE"];

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
        status: ["HEALTHY", "WARNING", "CRITICAL", "OFFLINE"][
          Math.floor(Math.random() * 4)
        ],
      }));

      const statusPriority = {
        CRITICAL: 1,
        WARNING: 2,
        HEALTHY: 3,
        OFFLINE: 4,
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

          {/* <FormControl>
            <InputLabel id="filter-status">Filtrar</InputLabel>
            <Select
              multiple
              value={filterStatus}
              onChange={(e) => {
                const value = e.target.value as string[];
                setFilterStatus(value);
              }}
              renderValue={(selected) => (selected as string[]).join(", ")}
              input={<OutlinedInput label="Filtrar" />}
              style={{ minWidth: 120 }}
            >
              {statusOptions.map((status) => (
                <MenuItem key={status} value={status}>
                  <Checkbox checked={filterStatus.includes(status)} />
                  {status}
                </MenuItem>
              ))}
            </Select>
          </FormControl> */}

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
          <DevicesList>
            {devices
              .filter((device) =>
                filterStatus.length > 0
                  ? filterStatus.includes(device.status)
                  : true
              )
              .map((device) => (
                <DeviceItem
                  key={device.id}
                  onClick={() => handleCellClick(device.id)}
                >
                  {device.status !== "OFFLINE" ? (
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
        )}
      </Container>
    </>
  );
};
