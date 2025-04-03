export interface VehicleProps {
    open: boolean;
    onClose: () => void;
    onSubmitted: () => void;
    vehicleId: number | null;
  }
  