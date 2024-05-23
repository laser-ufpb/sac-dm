export const isMenuItemActive = (path: string) => {
  return window.location.pathname.includes(path);
};
