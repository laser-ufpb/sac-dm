import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button, IconButton } from "@mui/material";
import { CustomModal } from "../../../components/CustomModal";
import {
  ModalContent,
  ModalFooter,
  ModalHeader,
} from "../../../components/CustomModal/styles";
import { Close } from "@mui/icons-material";
import { DefaultForm } from "../../../components/forms/DefaultForm";
import { FormGroup } from "../../../components/forms/FormGroup";
import {
  DefaultSelect,
} from "../../../components/forms/DefaultInput";
import { DeviceFormData, deviceSchema } from "./schema";
import DeviceService from "../../../app/services/devices";
import vehicleService from "../../../app/services/vehicle";
import { UpdateDeviceProps } from "./types";
import { useEffect, useState } from "react";

interface Vehicle {
  id: number;
  model: string;
  manufacturer: string;
}

export const UpdateDevice = ({ open, onClose, onSubmitted, deviceCode }: UpdateDeviceProps) => {
  const { control, handleSubmit, setValue } = useForm<DeviceFormData>({
    resolver: zodResolver(deviceSchema),
  });

  const [vehicles, setVehicles] = useState<Vehicle[]>([]);

  useEffect(() => {
    const fetchDevice = async () => {
      if (!deviceCode) return;
      try {
        const response = await DeviceService.getDeviceByCode(deviceCode);
        if (response) {
          setValue("device_code", response.device_code);
          setValue("vehicle_id", response.vehicle_id || 0);
        }
      } catch (error) {
        console.error(error);
      }
    };

    fetchDevice();
  }, [deviceCode, setValue]);

  useEffect(() => {
    const fetchVehicles = async () => {
      try {
        const response = await vehicleService.getVehicles();
        setVehicles(response);
      } catch (error) {
        console.error(error);
      }
    };

    fetchVehicles();
  }, []);

  const onSubmit = async (data: DeviceFormData) => {
    try {
      await DeviceService.putDevice(data);
      onSubmitted && onSubmitted();
      onClose();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <CustomModal open={open} onClose={onClose} size="sm">
      <ModalHeader>
        <h2>{deviceCode}</h2>
        <IconButton onClick={onClose}>
          <Close />
        </IconButton>
      </ModalHeader>
      <DefaultForm onSubmit={handleSubmit(onSubmit)}>
        <ModalContent>
          <FormGroup>
            <label htmlFor="vehicle_id">Veículo</label>
            <Controller
              name="vehicle_id"
              control={control}
              render={({ field }) => (
                <DefaultSelect
                  {...field}
                  onChange={(e) =>
                    setValue("vehicle_id", Number(e.target.value))
                  }
                >
                  <option value="" disabled>
                    Selecione um veículo
                  </option>
                  {vehicles.map((vehicle) => (
                    <option key={vehicle.id} value={vehicle.id}>
                      {vehicle.model} - {vehicle.manufacturer}
                    </option>
                  ))}
                </DefaultSelect>
              )}
            />
          </FormGroup>
        </ModalContent>
        <ModalFooter>
          <Button type="submit" variant="contained">
            Atualizar
          </Button>
        </ModalFooter>
      </DefaultForm>
    </CustomModal>
  );
};
