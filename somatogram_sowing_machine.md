# Somatogram Sowing Machine

A **Somatogram Sowing Machine** is a conceptual clinical-education system that "plants" body-map literacy into daily care by turning subjective body sensations into structured, interpretable somatograms over time.

## Core Idea
The machine combines guided check-ins, wearable signals, and anatomical mapping to help people and care teams answer:
- *Where* does a sensation happen?
- *How* does it feel?
- *When* does it appear, spread, or fade?
- *What* contexts (sleep, stress, food, movement, medication) are associated with it?

By repeatedly collecting this information, the system "sows" a high-resolution symptom timeline that supports earlier pattern detection and better communication.

## Functional Modules
1. **Input Console**
   - Touch or voice interface to annotate sensation type (pain, numbness, heat, pressure, itch, stiffness).
   - Body-surface sketch tool for region-level precision.

2. **Somatogram Engine**
   - Converts raw reports into layered maps (location, intensity, quality, duration).
   - Aligns reports across sessions to track movement, clustering, and recurrence.

3. **Context Integrator**
   - Links entries to optional streams (heart rate variability, sleep staging, activity load, hydration logs).
   - Flags likely correlates rather than claiming causation.

4. **Sowing Scheduler**
   - Sends lightweight prompts at useful intervals (e.g., morning baseline, post-activity, pre-sleep).
   - Adapts frequency to burden tolerance to reduce reporting fatigue.

5. **Insight Dashboard**
   - Produces clinician-friendly summaries: trend plots, body heat overlays, and trigger candidates.
   - Generates patient-facing language for shared decision making.

## Typical Use Cases
- **Chronic pain management:** distinguish persistent baseline discomfort from episodic flares.
- **Rehabilitation:** map recovery progression after injury or surgery.
- **Neurology follow-up:** monitor sensory changes with clearer temporal and spatial detail.
- **Behavioral medicine:** observe stress-linked somatic patterns and intervention response.

## Design Principles
- **Low-friction capture:** a check-in should take under one minute.
- **Interpretability first:** visualizations must remain understandable without technical training.
- **Consent-centered data flow:** users control sharing scope and retention.
- **Clinical humility:** outputs are decision-support artifacts, not diagnoses.

## Example Weekly Output
- Reduced shoulder-region stiffness intensity from 7/10 to 4/10 after mobility protocol.
- Evening forearm tingling appears on high keyboard-load days.
- Sleep below six hours predicts next-day diffuse neck discomfort.

## Limitations
- Self-report bias can distort maps when entries are delayed.
- Sensor correlations can be noisy in real-world settings.
- Body maps may miss deep or referred pain complexity.

## Future Extensions
- Multi-language symptom ontologies for cross-clinic interoperability.
- Federated analytics for privacy-preserving population trend learning.
- Adaptive coaching loops that recommend micro-interventions and track outcome shifts.
