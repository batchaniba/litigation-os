export const formatCurrency = (value: number, maximumFractionDigits = 0) =>
  new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits }).format(value);

export const formatNumber = (value: number) => new Intl.NumberFormat("en-US").format(value);

export const formatDate = (value: string | Date, options: Intl.DateTimeFormatOptions = { year: "numeric", month: "short", day: "numeric" }) =>
  new Intl.DateTimeFormat("en-US", options).format(value instanceof Date ? value : new Date(value));

export const formatMatterPath = (matterNumber: number) => `/matters/${matterNumber}`;
