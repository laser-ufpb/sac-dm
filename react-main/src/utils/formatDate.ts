export default function formatDate(datetimeStr: string): string {
  const date = new Date(datetimeStr);

  const options: Intl.DateTimeFormatOptions = {
    year: "numeric",
    month: "long",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  };

  return new Intl.DateTimeFormat("pt-BR", options).format(date);
}
