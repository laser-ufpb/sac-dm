import { useState } from "react";
import { ArrowDropDown } from "@mui/icons-material";
import { Checkbox } from "@mui/material";
import { SelectContainer, StyledOptions, StyledSelect } from "./styles";

interface OptionProps {
  id: number;
  description: string;
}

interface MultiSelectProps {
  label: string;
  options: OptionProps[];
  selectedOptions: number[];
  setSelectedOptions: React.Dispatch<React.SetStateAction<number[]>>;
}

export const MultiSelect: React.FC<MultiSelectProps> = ({
  label,
  options,
  selectedOptions,
  setSelectedOptions,
}) => {
  const [open, setOpen] = useState(false);

  const handleOptionChange = (id: number, isChecked: boolean) => {
    if (isChecked) {
      setSelectedOptions((prev) => [...prev, id]);
    } else {
      setSelectedOptions((prev) => prev.filter((item) => item !== id));
    }
  };

  const handleSelectNone = () => {
    setSelectedOptions([]);
  };

  return (
    <SelectContainer>
      <StyledSelect
        onClick={() => setOpen(!open)}
        style={{ borderRadius: open ? "8px 8px 0 0" : "8px" }}
      >
        {label}
        <ArrowDropDown />
      </StyledSelect>

      {open && (
        <StyledOptions>
          <div onClick={handleSelectNone} style={{ cursor: "pointer" }}>
            <Checkbox
              color="primary"
              checked={selectedOptions.length === 0}
              onChange={() => handleSelectNone()}
            />
            Nenhum
          </div>
          {options.map((option) => (
            <div key={option.id}>
              <Checkbox
                color="primary"
                checked={selectedOptions.includes(option.id)}
                onChange={(e) =>
                  handleOptionChange(option.id, e.target.checked)
                }
              />
              {option.description}
            </div>
          ))}
        </StyledOptions>
      )}
    </SelectContainer>
  );
};
