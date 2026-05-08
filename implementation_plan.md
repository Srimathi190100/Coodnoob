# NomadParis: Dynamic Travel & Experience Engine

NomadParis is a hyper-dynamic travel orchestration platform tailored for digital nomads in Paris. It adapts the traveler's itinerary in real-time based on environmental factors (weather, air quality), personal constraints (budget), and professional obligations (workload).

## User Review Required

> [!IMPORTANT]
> This plan involves creating a new backend configuration for Paris and a premium frontend dashboard.
> We will use the existing FastAPI structure but localized for Parisian geography and services.

## Proposed Changes

### Backend: Orchestration Engine

We will create a new configuration specific to Paris, mapping variables to localized adjustments.

#### [NEW] [config_paris.json](file:///Users/kiruthick/sri/config_paris.json)
- **Budget**: Shift from Michelin-star/expensive bistros to Boulangeries, Creperies, and public parks like Jardin du Luxembourg. Use the RATP (Metro/RER) exclusively.
- **Weather**: Adapt to "La Pluie Parisienne". Reroute to covered passages (Passage des Panoramas, Galerie Vivienne), museums (Louvre, Orsay), or cozy cafes with "un café" and Wi-Fi.
- **Workload**: Deploy to Station F, various "Anticafés", or libraries (BNF) for deep work.

#### [MODIFY] [app.py](file:///Users/kiruthick/sri/app.py)
- Update the `/health` and `/` endpoints to reflect the NomadParis branding.
- Add support for loading the Paris-specific config.

### Frontend: Nomad Dashboard

We will build a stunning, premium UI using Stitch.

#### [NEW] NomadParis UI
- **Landing Page**: A chic, high-end dashboard showing current "Nomad State" (Budget, Weather, Workload).
- **Dynamic Itinerary**: A visual timeline of the day's plans, highlighting real-time adjustments.
- **Experience Discovery**: A curated list of Paris experiences (Brutalist architecture in the 13th, art galleries in Le Marais).

## Verification Plan

### Automated Tests
- Test `/orchestrate` endpoint with Paris-specific state inputs.
- Verify UI consistency across light/dark modes in Stitch.

### Manual Verification
- Deploy to Google Cloud Run and verify the live instance.
