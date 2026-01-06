# Charger

## Overview
A charger converts available electrical power into a stable voltage and current profile that safely replenishes the energy storage of another device. Modern chargers often negotiate power levels dynamically to balance battery health, user experience, and grid efficiency.

## Common Types
- **Linear chargers**: Simple circuitry that drops voltage linearly; best for low-current or noise-sensitive applications.
- **Switch-mode chargers**: Use high-frequency switching to step voltages efficiently, enabling compact, cool-running adapters.
- **Inductive wireless chargers**: Transfer power through magnetic coupling, prioritizing convenience over peak efficiency.
- **USB Power Delivery (USB-PD) chargers**: Communicate over the USB-C connector to supply variable voltage/current profiles up to 240 W.

## Key Design Considerations
- **Safety**: Over-voltage, over-current, short-circuit, and thermal protections are essential to prevent device damage and fire risk.
- **Battery chemistry**: Charging profiles must match lithium-ion, lithium iron phosphate, nickel-metal hydride, or lead-acid characteristics.
- **Thermal management**: Component placement, heat sinks, and active control prevent overheating during fast charge cycles.
- **Power factor and efficiency**: High-efficiency topologies and power-factor correction minimize wasted energy and grid harmonics.
- **EMI compliance**: Filters, shielding, and controlled switching edges reduce electromagnetic interference for regulatory approval.

## USB-C Fast Charging Flow (Simplified)
1. Charger advertises supported power profiles via CC pins.
2. Device requests a profile (e.g., 9 V @ 3 A) based on battery and thermal status.
3. Charger adjusts output and monitors current and temperature.
4. Device throttles draw or falls back to lower profiles if limits are reached.

## Maintenance and Usage Tips
- Use certified cables that match the charger’s rated current to avoid voltage drop and overheating.
- Keep vents clear; elevated temperatures reduce charger lifespan.
- Unplug damaged adapters immediately and replace frayed cables.
- For long-term battery health, avoid sustained charging at maximum power unless necessary.

## Emerging Trends
- **GaN devices**: Gallium nitride transistors enable smaller, cooler, and higher-power-density chargers.
- **Bidirectional charging**: Future adapters may provide vehicle-to-load or device-to-device power sharing.
- **Adaptive algorithms**: Machine learning on-device can tailor charging curves to usage patterns for longevity.
