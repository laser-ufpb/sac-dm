import { Button, IconButton } from "@mui/material";
import { CustomModal } from "../../../components/CustomModal";
import {
  ModalContent,
  ModalFooter,
  ModalHeader,
} from "../../../components/CustomModal/styles";
import { Close } from "@mui/icons-material";
import { DefaultForm } from "../../../components/forms/DefaultForm";
import { useEffect, useState } from "react";
import VehicleService from "../../../app/services/vehicle";
import { VehicleProps } from "./types";

interface Vehicle {
  id: number;
  model: string;
  manufacturer: string;
}

export const DeleteVehicle = ({ open, onClose, onSubmitted, vehicleId }: VehicleProps) => {
  const [vehicle, setVehicle] = useState<Vehicle | null>(null);

  useEffect(() => {
    if (open) {
      const fetchVehicle = async () => {
        if (!vehicleId) return;
        try {
          const response = await VehicleService.getVehicleById(vehicleId);
          if (response) {
            setVehicle(response);
          }
        } catch (error) {
          console.error(error);
        }
      };
  
      fetchVehicle();
    }
  }, [open, vehicleId]); 
  

  const handleDeleteVehicle = async () => {
    if (!vehicleId) {
      console.error("ID do veículo não fornecido.");
      return; 
    }
  
    try {
      await VehicleService.deleteVehicleById(vehicleId); 
      onSubmitted && onSubmitted(); // Chama a função de callback
      onClose(); 
    } catch (error) {
      console.error("Erro ao deletar veículo:", error);
    }
  };

  return (
    <CustomModal open={open} onClose={onClose} size="sm">
      <ModalHeader>
        <h2>Deletar veículo: {vehicle?.model}</h2>
        <IconButton onClick={onClose}>
          <Close />
        </IconButton>
      </ModalHeader>
      <DefaultForm onSubmit={(e) => e.preventDefault()}>
        <ModalContent>
          <label>Tem certeza que deseja deletar o veículo {vehicle?.model} ({vehicle?.manufacturer})?</label>
        </ModalContent>
        <ModalFooter>
          <Button type="button" variant="contained" color="error" onClick={handleDeleteVehicle}>
            Deletar
          </Button>
        </ModalFooter>
      </DefaultForm>
    </CustomModal>
  );
};
