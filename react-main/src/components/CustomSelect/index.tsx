import React, { useState, useEffect } from "react";
import { ArrowDropDown } from "@mui/icons-material";
import { SelectContainer, StyledOptions, StyledSelect } from "./styles";

interface OptionProps {
  id: number;
  description: string;
}

interface CustomSelectProps {
  label: string;
  options: OptionProps[];
  selectedOption: number | null;
  setSelectedOption: React.Dispatch<React.SetStateAction<number | null>>;
}

export const CustomSelect: React.FC<CustomSelectProps> = ({
  label,
  options,
  selectedOption,
  setSelectedOption,
}) => {
  const [open, setOpen] = useState(false);
  const [selectedDescription, setSelectedDescription] = useState<string>("");

  useEffect(() => {
    const selectedOptionObj = options.find(
      (option) => option.id === selectedOption
    );
    if (selectedOptionObj) {
      setSelectedDescription(selectedOptionObj.description);
    } else {
      setSelectedDescription("");
    }
  }, [selectedOption, options]);

  const handleOptionChange = (id: number) => {
    setSelectedOption(id);
    setOpen(false);
  };

  return (
    <SelectContainer>
      <StyledSelect
        onClick={() => setOpen(!open)}
        style={{ borderRadius: open ? "8px 8px 0 0" : "8px" }}
      >
        {selectedDescription || label}
        <ArrowDropDown />
      </StyledSelect>

      {open && (
        <StyledOptions>
          {options.map((option) => (
            <div
              key={option.id}
              onClick={() => handleOptionChange(option.id)}
              className={selectedOption === option.id ? "selected" : ""}
            >
              {option.description}
            </div>
          ))}
        </StyledOptions>
      )}
    </SelectContainer>
  );
};
