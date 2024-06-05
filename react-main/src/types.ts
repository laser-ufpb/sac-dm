export interface VehicleProps {
  manufacturer: string;
  model: string;
  engine_type: string | null; // Usamos string | null para representar "null" como um valor válido
  status_id: number | null; // Permitimos que status_id seja number ou null
  id: number;
  manufacture_year: number;
  number_of_engines: number;
}
