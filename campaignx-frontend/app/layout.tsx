import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { QueryProvider } from "@/components/QueryProvider";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "CampaignX AI - Multi-Agent Email Optimization",
  description: "Production-grade AI-powered email campaign optimization system",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} font-sans antialiased`}>
        <QueryProvider>{children}</QueryProvider>
      </body>
    </html>
  );
}
