export interface TableColumn {
  id: string;
  label: string;
}

export interface TableData {
  [key: string]: any;
}

export interface CustomTableProps {
  columns: TableColumn[];
  data: TableData[];
  isLoading?: boolean;
  onCellClick?: (id: number) => void;
}
