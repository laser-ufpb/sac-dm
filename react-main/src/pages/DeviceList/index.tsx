import { useEffect, useState } from "react";
import { DeviceProps, VehicleProps, StatusProps } from "../../types";
import {
  DeviceItem,
  DevicesList,
  Header,
  NoDevicesMessage,
  SectionTitle,
  FilterContainer,
  DeleteButton,
  OnOffButton,
} from "./styles";
import { Button, CircularProgress, Menu, MenuItem} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import SettingsPowerIcon from '@mui/icons-material/SettingsPower';
import { AddCircle, AirplanemodeActive, DeviceHub} from "@mui/icons-material";
import { AddDevice } from "./AddDevice";
import { AddVehicle } from "./AddVehicle";
import { UpdateDevice } from "./UpdateDevice";
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
  const [selectedDeviceCode, setSelectedDeviceCode] = useState<string | null>(null);
  const [openUpdateDeviceModal, setOpenUpdateDeviceModal] = useState(false);
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

  const handleDelete = async (deviceCode: string) => {
    try {
      await deviceService.DeleteDevice(deviceCode); // Chama a API para deletar
      setDevices((prevDevices) =>
        prevDevices.filter((device) => device.device_code !== deviceCode)
      ); // Remove o dispositivo deletado da lista
    } catch (error) {
      console.error("Erro ao deletar dispositivo:", error);
    }
  };

  const onOffDevice = async (deviceCode: string) => {
    try {
        const device = await deviceService.getDeviceByCode(deviceCode);
        
        if (!device || typeof device.status_id === 'undefined') {
            console.error("Dispositivo não encontrado ou status_id indefinido");
            return;
        }
        
        const newStatusId = device.status_id === 1 ? 2 : 1;
        
        const data = {
            device_code: deviceCode,
            status_id: newStatusId,
            vehicle_id: device.vehicle_id
        };
        
        await deviceService.putDevice(data);

        // Atualiza os dispositivos na página sem recarregá-la
        setDevices((prevDevices: any[]) =>
          prevDevices.map(d => d.device_code === deviceCode ? { ...d, status_id: newStatusId } : d)
      );
    } catch (error) {
        console.error("Erro ao atualizar status do dispositivo", error);
    }
};

  const handleCellClick = (id: number, type: string) => {
    navigate(`/${type}/${id}`);
  };

  const filteredDevices = Array.isArray(devices)
    ? devices.filter((device) =>
        filterStatus.length > 0 ? filterStatus.includes(device.status_id) : true
      )
    : [];

  const filteredVehicles = Array.isArray(vehicles)
    ? vehicles.filter((vehicle) =>
        filterStatus.length > 0
          ? filterStatus.includes(vehicle.status_id)
          : true
      )
    : [];

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
      <UpdateDevice
        open={openUpdateDeviceModal}
        onClose={() => setOpenUpdateDeviceModal(false)}
        deviceCode={selectedDeviceCode}
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
              options={
                Array.isArray(statusOptions)
                  ? statusOptions.map((status: StatusProps) => ({
                      id: status.id,
                      description: status.description,
                    }))
                  : []
              }
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
                  onClick={() => {
                    setSelectedDeviceCode(device.device_code);
                    setOpenUpdateDeviceModal(true);
                  }}>
                  <OnOffButton
                    onClick={(e) => {
                      e.stopPropagation();
                      onOffDevice(device.device_code);
                    }}
                  >
                    <SettingsPowerIcon />
                  </OnOffButton>
                  <DeleteButton
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDelete(device.device_code);
                    }}
                  >
                    <DeleteIcon />
                  </DeleteButton>
                  
                  {/* Ícone principal do dispositivo */}
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
