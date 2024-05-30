import React from "react";
import { SelectContainer } from "../../styles/select";

interface DataCountSelectProps {
  dataCount: number;
  setDataCount: (value: number) => void;
}

const DataCountSelect: React.FC<DataCountSelectProps> = ({
  dataCount,
  setDataCount,
}) => {
  return (
    <SelectContainer>
      <label htmlFor="dataCount">Mostrar últimos: </label>
      <select
        id="dataCount"
        value={dataCount}
        onChange={(e) => setDataCount(Number(e.target.value))}
      >
        <option value={10}>10</option>
        <option value={50}>50</option>
        <option value={100}>100</option>
        <option value={200}>200</option>
        <option value={1000}>1000</option>
      </select>
    </SelectContainer>
  );
};

export default DataCountSelect;
