import type { Metadata } from "next";
import "./globals.css";

import { inter } from "@/app/ui/fonts";
import LayoutWrapper from "@/app/ui/components/layout-wrapper";

export const metadata: Metadata = {
  title: "TT Scraper - Table Tennis Equipment Tracker",
  description: "Track and compare table tennis equipment prices across multiple stores",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} antialiased`}>
        <LayoutWrapper>
          {children}
        </LayoutWrapper>
      </body>
    </html>
  );
}
