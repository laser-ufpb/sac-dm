import React, { useEffect, useState } from "react";
import statusService from "../../../../app/services/status";
import { StatusProps } from "../../../../types";
import { MultiSelect } from "../../../../components/MultiSelect";

interface FilterStatusProps {
  filterStatus: number[];
  setFilterStatus: React.Dispatch<React.SetStateAction<number[]>>;
}

export const FilterStatus: React.FC<FilterStatusProps> = ({
  filterStatus,
  setFilterStatus,
}) => {
  const [statusOptions, setStatusOptions] = useState<StatusProps[]>([]);

  useEffect(() => {
    const loadStatus = async () => {
      try {
        const response = await statusService.getStatus();
        setStatusOptions(response);
      } catch (error) {
        console.error(error);
      }
    };

    loadStatus();
  }, []);

  return (
    <MultiSelect
      label="Filtrar"
      options={statusOptions}
      selectedOptions={filterStatus}
      setSelectedOptions={setFilterStatus}
    />
  );
};
