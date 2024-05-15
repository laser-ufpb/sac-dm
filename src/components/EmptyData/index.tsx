import { Container } from "./styles";

export const EmptyData = ({ message }: { message: string }) => {
  return (
    <Container>
      <p>{message}</p>
    </Container>
  );
};
