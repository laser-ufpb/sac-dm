export interface VehicleProps {
  manufacturer: string;
  model: string;
  engine_type: string | null; // Usamos string | null para representar "null" como um valor válido
  status_id: number;
  id: number;
  manufacture_year: number;
  number_of_engines: number;
}

export interface DeviceProps {
  device_code: string;
  id: number;
  timestamp: string;
  status_id: number;
}

export interface StatusProps {
  description: string;
  id: number;
}
