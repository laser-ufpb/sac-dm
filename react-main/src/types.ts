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
  status_id: number;
  timestamp: string;
  vehicle_id: number;
  id: number;
}

export interface StatusProps {
  description: string;
  id: number;
}

export interface SacDmDefaultProps {
  x_standard_deviation: number;
  y_standard_deviation: number;
  z_standard_deviation: number;
  x_mean: number;
  y_mean: number;
  z_mean: number;
  id: number;
  vehicle_id: number;
}
