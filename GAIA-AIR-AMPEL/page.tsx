import { AirQualityDashboard } from "@/components/air-quality-dashboard"

export default function Home() {
  return (
    <div className="container mx-auto py-6">
      <h1 className="text-3xl font-bold mb-6">GAIA-AIR-AMPEL Dashboard</h1>
      <AirQualityDashboard />
    </div>
  )
}

