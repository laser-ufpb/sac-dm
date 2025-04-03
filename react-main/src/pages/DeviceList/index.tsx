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
  OnOffContainer,
  OnOffLabel,
} from "./styles";
import { Button, CircularProgress, Menu, MenuItem} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import SettingsPowerIcon from '@mui/icons-material/SettingsPower';
import { AddCircle, AirplanemodeActive, DeviceHub} from "@mui/icons-material";
import { AddDevice } from "./AddDevice";
import { AddVehicle } from "./AddVehicle";
import { UpdateDevice } from "./UpdateDevice";
import { DeleteDevice } from "./DeleteDevice";
import { DeleteVehicle } from "./DeleteVehicle";
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
  const [selectedVehicleCode, setSelectedVehicleCode] = useState<number | null>(null);
  const [openUpdateDeviceModal, setOpenUpdateDeviceModal] = useState(false);
  const [openDeleteDeviceModal, setOpenDeleteDeviceModal] = useState(false);
  const [openDeleteVehicleModal, setOpenDeleteVehicleModal] = useState(false);
  const [filterStatus, setFilterStatus] = useState<number[]>([]);
  const [statusOptions, setStatusOptions] = useState<StatusProps[]>([]);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [blinkingColor, setBlinkingColor] = useState("#1E88E5");
  const [transitionStyle] = useState({ transition: "color 1s ease-in-out" });

  const navigate = useNavigate();

  useEffect(() => {
    loadItems();
    loadStatusOptions();
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setBlinkingColor((prevColor) => (prevColor === "#1E88E5" ? "#9AA0A6" : "#1E88E5"));
    }, 800);
    return () => clearInterval(interval);
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

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const deviceResponse: DeviceProps[] = await deviceService.getDevices();
  
        // Verifica se há mudanças nos status antes de atualizar o estado
        const hasChanges = deviceResponse.some((newDevice: DeviceProps) => {
          const currentDevice = devices.find((d) => d.device_code === newDevice.device_code);
          return currentDevice && currentDevice.status_id !== newDevice.status_id;
        });
  
        if (hasChanges) {
          setDevices(deviceResponse); // Atualiza somente se houver mudanças
        }
      } catch (error) {
        console.error("Erro ao atualizar dispositivos:", error);
      }
    }, 5000);
  
    return () => clearInterval(interval); // Limpa o intervalo ao desmontar o componente
  }, [devices]); // Observa 'devices' para detectar mudanças

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
      <DeleteDevice
        open={openDeleteDeviceModal}
        onClose={() => setOpenDeleteDeviceModal(false)}
        deviceCode={selectedDeviceCode}
        onSubmitted={loadItems}
      />
      <DeleteVehicle
        open={openDeleteVehicleModal}
        onClose={() => setOpenDeleteVehicleModal(false)}
        vehicleId={selectedVehicleCode}
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
                  <OnOffContainer>
                    <OnOffButton
                      onClick={(e) => {
                        e.stopPropagation();
                        onOffDevice(device.device_code);
                      }}
                    >
                      <SettingsPowerIcon
                        sx={{
                          color: device.status_id === 2 ? blinkingColor : getStatusColor(device.status_id, statusOptions),
                          ...transitionStyle,
                        }}
                      />
                    </OnOffButton>
                      
                    {device.status_id === 2 && <OnOffLabel>Ligando...</OnOffLabel>}
                  </OnOffContainer>
                  <DeleteButton
                    onClick={(e) => {
                      e.stopPropagation();
                      setSelectedDeviceCode(device.device_code);
                      setOpenDeleteDeviceModal(true);
                      // handleDeleteDevice(device.device_code);
                    }}
                  >
                    <DeleteIcon />
                  </DeleteButton>
                  
                  {/* Ícone principal do dispositivo */}
                  <DeviceHub
                    sx={{ color: device.status_id === 2 ? blinkingColor : getStatusColor(device.status_id, statusOptions),...transitionStyle,}}
                  />
                  {/* <DeviceHub
                    sx={{
                      color: getStatusColor(device.status_id, statusOptions),
                    }}
                  /> */}
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

                  <DeleteButton
                    onClick={(e) => {
                      e.stopPropagation();
                      setSelectedVehicleCode(vehicle.id);
                      setOpenDeleteVehicleModal(true);
                      // handleDeleteDevice(device.device_code);
                    }}
                  >
                    <DeleteIcon />
                  </DeleteButton>
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
