# Privacy-protected inter-hospital patient file transfer system (中国)

This document outlines a reference design for securely exchanging patient files between hospitals within China while meeting local privacy, data localization, and cybersecurity requirements. It favors standards-based interoperability, strong cryptography, and verifiable auditability so that clinical workflows can be automated without exposing protected health information (PHI).

## Objectives
- Ensure confidentiality, integrity, and availability of medical files exchanged across institutions.
- Align with China-specific regulations (个人信息保护法 PIPL, 数据安全法 DSL, 网络安全法 CSL, and MLPS 2.0) and healthcare guidance for medical data classification.
- Provide traceable consent/authorization handling and a defensible audit trail.
- Support interoperability with common healthcare standards (FHIR/HL7, DICOM) and hospital information systems (HIS, LIS, PACS).
- Facilitate operational resilience (resumable transfers, queued delivery, redundancy) across metropolitan and regional networks.

## Regulatory & policy alignment
- **Data localization and sovereignty:** Persist PHI and encryption keys only on infrastructure physically located in mainland China; use region-scoped object storage and domestic KMS/HSM.
- **Classified data handling:** Treat PHI as Important Data; apply MLPS 2.0 level 3 or above controls (access control, security baselines, vulnerability management, security monitoring).
- **Consent management:** Bind each transfer request to signed patient consent or lawful treatment basis; include consent IDs in transfer metadata and audit events.
- **Minimum necessary disclosure:** Default to sending de-identified or pseudonymized datasets; permit re-identification only at the receiving hospital with appropriate keys/claims.
- **Cross-border blocking:** Explicitly block cross-border routing; enforce egress controls and geo-fencing on network edges and storage endpoints.
- **Retention and deletion:** Enforce configurable retention windows and cryptographic erasure upon expiry or withdrawal of consent.

## High-level architecture
```
[Sender HIS/LIS/PACS] --(FHIR/DICOM)--> [Hospital Edge Gateway] --mTLS/TLS 1.3--> [Transfer Coordinator] --mTLS--> [Receiver Edge Gateway] --(FHIR/DICOM)--> [Receiver HIS/LIS/PACS]
                                         |                                       
                                         |--> [Audit & SIEM]
                                         |--> [KMS/HSM + Key Broker]
                                         '--> [Message Queue/Object Storage]
```

### Core components
- **Hospital Edge Gateway (appliance or container):**
  - Adapts local systems (HIS/LIS/PACS) via FHIR/HL7/DICOM connectors.
  - Performs data minimization, de-identification, digital signing, and envelope encryption before egress.
  - Enforces DLP policies (regex/ML-based PHI detection) and blocks non-compliant payloads.
  - Supports resumable, chunked uploads with checksums.
- **Transfer Coordinator (central or regional service):**
  - Orchestrates transfer sessions, issues short-lived pre-signed upload/download URLs, and manages delivery state.
  - Stores only encrypted blobs plus minimal metadata (no PHI) in message queues/object storage with region pinning.
  - Performs policy evaluation (consent validity, purpose-of-use, receiving hospital entitlement, data residency).
- **KMS/HSM + Key Broker:**
  - Generates and protects keys using SM2/SM4 or AES-GCM suites; supports dual-control key operations.
  - Implements envelope encryption (per-file DEK encrypted by hospital KEK) and optional attribute-based encryption (ABE) for purpose-scoped access.
- **Identity and Access Management:**
  - Mutual TLS with hospital-issued client certs; OIDC/SAML integration for staff identity.
  - Role- and attribute-based access control (RBAC/ABAC) with least-privilege and separation of duties.
- **Audit, monitoring, and compliance:**
  - Immutable, signed logs shipped to centralized SIEM; log schema includes consent ID, purpose-of-use, data class, hash of payload, and policy decision.
  - Continuous compliance checks (configuration drift, vulnerability scans, CMDB reconciliation).

## Security and privacy controls
- **Transport security:** TLS 1.3 with modern cipher suites; support GM/T 0024-2014 algorithms where required. Enforce HSTS, OCSP stapling, and certificate pinning between gateways and coordinator.
- **Data encryption:**
  - **At rest:** AES-256-GCM or SM4-GCM with per-file DEKs; KEKs stored in HSM-backed KMS. Store encrypted files in region-scoped object storage with bucket policies blocking public access.
  - **In use:** Decrypt only inside secure enclaves (e.g., SGX/TEE) when processing sensitive data; otherwise stream directly to receiving systems.
- **Integrity and authenticity:**
  - Sign payload manifests with sender private key; include SHA-256/SM3 checksums per chunk.
  - Use signed tokens (JWT or GM/T 0107 equivalents) with short TTL for transfer authorization.
- **De-identification pipeline:**
  - Structured data: remove direct identifiers, apply tokenization/pseudonymization via format-preserving encryption, and perturb quasi-identifiers.
  - Imaging (DICOM): strip or rewrite sensitive tags; optionally apply burned-in PHI detection using OCR/vision model before transfer.
- **Access governance:**
  - Policy engine (OPA/Casbin) enforces consent, purpose-of-use, and break-glass workflows.
  - Mandatory multi-factor authentication for manual approvals; delegated authorization with signed approvals for emergency access.
- **Resilience and reliability:**
  - Chunked, checkpointed transfers with resume tokens; background verification of checksums after reassembly.
  - Multi-AZ deployment within China; message queues for asynchronous delivery to handle intermittent links.

## Data model and API surface (illustrative)
- **Transfer request (POST /transfers):**
  - Metadata: patient pseudonym/ID token, consent_id, purpose_of_use, data_classification, retention_until, receiver_hospital_id.
  - Payload manifest: file list with hashes, sizes, and sensitivity tags.
  - Policy decision recorded with unique transfer_id and pre-signed upload URL (short-lived, single-use).
- **Chunk upload (PUT presigned_url):**
  - Client-supplied chunk hashes; server validates length, checksum, and token scope.
- **Finalize (POST /transfers/{id}/complete):**
  - Reassembles chunks, verifies manifest, stores encrypted blob, dispatches notification to receiver queue.
- **Retrieval (GET /transfers/{id}/download):**
  - Receiver presents mTLS cert + OIDC token; coordinator checks entitlement, consent freshness, and retention; issues pre-signed download.
- **Audit stream (/audit/events):**
  - Append-only feed consumable by SIEM; events include cryptographic proofs (hashes, signatures) and decision outcomes.

## Operational controls
- **Onboarding:** Vet hospital identity, provision client certificates, register network ranges, and configure data classes permitted for each partner.
- **DLP and policy tuning:** Maintain centrally managed rule sets with hospital-specific overrides; periodically validate against red-team scenarios.
- **Key management lifecycle:** Rotation schedules, escrow policies, split knowledge for key custodians, and mandatory HSM-backed backups.
- **Incident response:** Playbooks for suspected data leakage, compromised credentials, or failed integrity checks; rapid revocation of certs/tokens.
- **Observability:** Metrics on transfer latency, failure rates, and policy denials; SLO/SLI dashboards with alerting.

## Risk analysis (selected threats and mitigations)
- **Man-in-the-middle or spoofed hospital:** mTLS with pinned certs; certificate revocation checks; session binding to cert fingerprint.
- **Unauthorized re-identification:** Enforce de-identification defaults, ABE-scoped decryption keys, and purpose-of-use enforcement.
- **Data exfiltration via misconfigured storage:** Private buckets, VPC endpoints, egress filtering, continuous configuration scanning.
- **Compromised operator account:** Least-privilege RBAC, hardware-backed MFA, just-in-time elevation with approval, audit of admin actions.
- **Ransomware on edge gateway:** Immutable backups of configurations, signed software supply chain, runtime sandboxing, and behavior-based malware detection.

## Deployment considerations (China-specific)
- Deploy on mainland cloud regions (e.g., Alibaba Cloud, Tencent Cloud) with government-approved cryptography modules.
- Integrate with local PKI providers for SM-series certificates; support GMSSL stacks where mandated.
- Maintain bilingual UI (Chinese/English) and localized consent artifacts; store consent proofs per regulatory templates.
- Validate vendors and cross-hospital links against CSL critical information infrastructure (CII) requirements.

## Minimal pilot rollout
1. Stand up Transfer Coordinator and KMS in a mainland region with MLPS Level 3 controls.
2. Deploy Edge Gateways at two partner hospitals with DICOM/FHIR connectors and DLP enabled.
3. Configure mTLS trust, consent verification hooks, and SIEM forwarding.
4. Execute test transfers (de-identified imaging + structured lab data) with checksum/audit validation.
5. Conduct third-party security assessment and MLPS filing before production scaling.
