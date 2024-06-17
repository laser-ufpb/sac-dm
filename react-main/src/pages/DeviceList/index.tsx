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
import { Button, CircularProgress, Menu, MenuItem } from "@mui/material";
import { AddCircle, AirplanemodeActive, DeviceHub } from "@mui/icons-material";
import { AddDevice } from "./AddDevice";
import { AddVehicle } from "./AddVehicle";
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
  const [openAddVehicleModal, setOpenAddVehicleModal] = useState(false);
  const [filterStatus, setFilterStatus] = useState<number[]>([]);
  const [statusOptions, setStatusOptions] = useState<StatusProps[]>([]);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

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

  const filteredVehicles = vehicles.filter((vehicle) => {
    return filterStatus.length > 0
      ? filterStatus.includes(vehicle.status_id)
      : true;
  });

  const handleAddClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  return (
    <>
      <AddDevice
        open={openAddDeviceModal}
        onClose={() => setOpenAddDeviceModal(false)}
        onSubmitted={loadItems}
      />
      <AddVehicle
        open={openAddVehicleModal}
        onClose={() => setOpenAddVehicleModal(false)}
        onSubmitted={loadItems}
      />
      <Header>
        <h2>Gerenciamento de Dispositivos e Veículos</h2>
        <Button
          variant="contained"
          startIcon={<AddCircle />}
          onClick={handleAddClick}
        >
          <p>Adicionar Dispositivo/Veículo</p>
        </Button>
        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleMenuClose}
        >
          <MenuItem
            onClick={() => {
              setOpenAddDeviceModal(true);
              handleMenuClose();
            }}
          >
            Adicionar Dispositivo
          </MenuItem>
          <MenuItem
            onClick={() => {
              setOpenAddVehicleModal(true);
              handleMenuClose();
            }}
          >
            Adicionar Veículo
          </MenuItem>
        </Menu>
      </Header>

      {isLoading ? (
        <CircularProgress />
      ) : (
        <>
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
          <SectionTitle>Dispositivos:</SectionTitle>
          {filteredDevices.length > 0 ? (
            <DevicesList>
              {filteredDevices.map((device) => (
                <DeviceItem
                  key={device.id}
                  // onClick={() => handleCellClick(device.id, "device")}
                >
                  <DeviceHub
                    sx={{
                      color: getStatusColor(device.status_id, statusOptions),
                    }}
                  />
                  <h3>{device.device_code}</h3>
                </DeviceItem>
              ))}
            </DevicesList>
          ) : (
            <NoDevicesMessage>Nenhum dispositivo encontrado</NoDevicesMessage>
          )}
          <SectionTitle>Veículos:</SectionTitle>
          {filteredVehicles.length > 0 ? (
            <DevicesList>
              {filteredVehicles.map((vehicle) => (
                <DeviceItem
                  key={vehicle.id}
                  onClick={() => handleCellClick(vehicle.id, "vehicle")}
                >
                  <AirplanemodeActive
                    sx={{
                      color: getStatusColor(vehicle.status_id, statusOptions),
                    }}
                  />
                  <h3>
                    {vehicle.model} - {vehicle.manufacturer}
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
