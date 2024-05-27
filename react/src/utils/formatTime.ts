export const formatTime = (timestamp: string): string => {
  const correctedTimestamp = timestamp.substring(0, 13); // Pega apenas os 13 primeiros dígitos
  const date = new Date(Number(correctedTimestamp)); // Converte para Date
  return date.toLocaleString(); // Retorna a data formatada como string
};