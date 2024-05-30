import { ArrowDropDown } from "@mui/icons-material";
import {
  Container,
  SelectContainer,
  StyledOptions,
  StyledSelect,
} from "./styles";
import { useEffect, useState } from "react";
import { Checkbox } from "@mui/material";
import statusService from "../../../../app/services/status";
import { StatusProps } from "./types";

interface FilterStatusProps {
  filterStatus: number[];
  setFilterStatus: React.Dispatch<React.SetStateAction<number[]>>;
}

export const FilterStatus: React.FC<FilterStatusProps> = ({
  filterStatus,
  setFilterStatus,
}) => {
  const [open, setOpen] = useState(false);
  const [statusOptions, setStatusOptions] = useState<StatusProps[]>([]);

  useEffect(() => {
    loadStatus();
  }, []);

  const loadStatus = async () => {
    try {
      const response = await statusService.getStatus();
      setStatusOptions(response);
    } catch (error) {
      console.error(error);
    }
  }

  const handleStatusChange = (status: number, isChecked: boolean) => {
    if (isChecked) {
      setFilterStatus((prevStatus) => [...prevStatus, status]);
    } else {
      setFilterStatus((prevStatus) =>
        prevStatus.filter((item) => item !== status)
      );
    }
  };

  return (
    <Container>
      <SelectContainer>
        <StyledSelect
          onClick={() => setOpen(!open)}
          style={{ borderRadius: open ? "8px 8px 0 0" : "8px" }}
        >
          Filtrar
          <ArrowDropDown />
        </StyledSelect>

        {open && (
          <StyledOptions>
            {statusOptions.map((status: StatusProps) => (
              <div key={status.id}>
                <Checkbox
                  color="primary"
                  checked={filterStatus.includes(status.id)}
                  onChange={(e) => handleStatusChange(status.id, e.target.checked)}
                />
                {status.description}
              </div>
            ))}
          </StyledOptions>
        )}
      </SelectContainer>
    </Container>
  );
};
