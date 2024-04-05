import { ArrowDropDown } from "@mui/icons-material";
import { Container, StyledOptions, StyledSelect } from "./styles";
import { useState } from "react";
import { Checkbox } from "@mui/material";

interface FilterStatusProps {
  statusOptions: string[];
  filterStatus: string[];
  setFilterStatus: React.Dispatch<React.SetStateAction<string[]>>;
}

export const FilterStatus: React.FC<FilterStatusProps> = ({
  statusOptions,
  filterStatus,
  setFilterStatus,
}) => {
  const [open, setOpen] = useState(false);

  const handleStatusChange = (status: string, isChecked: boolean) => {
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
      <StyledSelect
        onClick={() => setOpen(!open)}
        style={{ borderRadius: open ? "8px 8px 0 0" : "8px" }}
      >
        Filtrar
        <ArrowDropDown />
      </StyledSelect>

      {open && (
        <StyledOptions>
          {statusOptions.map((status: string) => (
            <div key={status}>
              <Checkbox
                color="primary"
                checked={filterStatus.includes(status)}
                onChange={(e) => handleStatusChange(status, e.target.checked)}
              />
              {status}
            </div>
          ))}
        </StyledOptions>
      )}
    </Container>
  );
};
