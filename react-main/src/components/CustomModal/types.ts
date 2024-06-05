export interface ModalProps {
  open: boolean;
  onClose: () => void;
  children: React.ReactNode;
  size?: "xsm" | "sm" | "md" | "lg" | "xl";
}
