import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Alignment Review",
  description: "A presentational review of an epistemic alignment dossier.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
