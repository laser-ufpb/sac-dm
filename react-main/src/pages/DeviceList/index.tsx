import { useEffect, useState } from "react";
import { DeviceProps, VehicleProps, StatusProps } from "../../types";
import {
  DeviceItem,
  DevicesList,
  Header,
  NoDevicesMessage,
  SectionTitle,
  FilterContainer,
} from "./styles";
import { Button, CircularProgress } from "@mui/material";
import {
  AddCircle,
  AirplanemodeActive,
  AirplanemodeInactive,
  DirectionsCarFilled,
} from "@mui/icons-material";
import { AddDevice } from "./AddDevice";
import { useNavigate } from "react-router-dom";
import { getStatusColor } from "../../utils/getStatusColor";
import { MultiSelect } from "../../components/MultiSelect";
import deviceService from "../../app/services/devices";
import statusService from "../../app/services/status";
import vehicleService from "../../app/services/vehicle";

export const DeviceList = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [devices, setDevices] = useState<DeviceProps[]>([]);
  const [vehicles, setVehicles] = useState<VehicleProps[]>([]);
  const [openAddDeviceModal, setOpenAddDeviceModal] = useState(false);
  const [filterStatus, setFilterStatus] = useState<number[]>([]);
  const [statusOptions, setStatusOptions] = useState<StatusProps[]>([]);

  const navigate = useNavigate();

  useEffect(() => {
    loadItems();
    loadStatusOptions();
  }, []);

  const loadItems = async () => {
    setIsLoading(true);
    try {
      const [deviceResponse, vehicleResponse] = await Promise.all([
        deviceService.getDevices(),
        vehicleService.getVehicles(),
      ]);

      setDevices(deviceResponse);
      setVehicles(vehicleResponse);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadStatusOptions = async () => {
    try {
      const response = await statusService.getStatus();
      setStatusOptions(response);
    } catch (error) {
      console.error(error);
    }
  };

  const handleCellClick = (id: number, type: string) => {
    navigate(`/${type}/${id}`);
  };

  const filteredDevices = devices.filter((device) => {
    return filterStatus.length > 0
      ? filterStatus.includes(device.status_id)
      : true;
  });

  return (
    <>
      <AddDevice
        open={openAddDeviceModal}
        onClose={() => setOpenAddDeviceModal(false)}
        onSubmitted={loadItems}
      />
      <Header>
        <h2>Gerenciamento de Dispositivos e Veículos</h2>
        <Button
          variant="contained"
          startIcon={<AddCircle />}
          onClick={() => setOpenAddDeviceModal(true)}
        >
          <p>Adicionar Dispositivo/Veículo</p>
        </Button>
      </Header>

      {isLoading ? (
        <CircularProgress />
      ) : (
        <>
          <SectionTitle>Dispositivos:</SectionTitle>
          <FilterContainer>
            <MultiSelect
              label="Filtrar"
              options={statusOptions.map((status: StatusProps) => ({
                id: status.id,
                description: status.description,
              }))}
              selectedOptions={filterStatus}
              setSelectedOptions={setFilterStatus}
            />
          </FilterContainer>
          {filteredDevices.length > 0 ? (
            <DevicesList>
              {filteredDevices.map((device) => (
                <DeviceItem
                  key={device.id}
                  onClick={() => handleCellClick(device.id, "device")}
                >
                  {device.status_id ? (
                    <AirplanemodeActive
                      sx={{
                        color: getStatusColor(device.status_id, statusOptions),
                      }}
                    />
                  ) : (
                    <AirplanemodeInactive
                      sx={{
                        color: getStatusColor(device.status_id, statusOptions),
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
          <SectionTitle>Veículos:</SectionTitle>
          {vehicles.length > 0 ? (
            <DevicesList>
              {vehicles.map((vehicle) => (
                <DeviceItem
                  key={vehicle.id}
                  onClick={() => handleCellClick(vehicle.id, "vehicle")}
                >
                  <DirectionsCarFilled
                    sx={{
                      color: getStatusColor(vehicle.status_id, statusOptions),
                    }}
                  />
                  <h3>
                    {vehicle.manufacturer} {vehicle.model}
                  </h3>
                </DeviceItem>
              ))}
            </DevicesList>
          ) : (
            <NoDevicesMessage>Nenhum veículo encontrado</NoDevicesMessage>
          )}
        </>
      )}
    </>
  );
};
