export interface FilterStatusProps {
  statusOptions: string[];
  setFilterStatus: (status: string[]) => void;
}

export interface StatusProps {
  description: string;
  id: number;
}