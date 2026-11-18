# First Responder SOP - Suspected Ransomware in a Healthcare Network

Case: OMEGA-2026-11. Purpose: preserve evidence and patient safety during the first hours of a ransomware incident.

## 1. Arrive and take command

1. Confirm authority (incident commander, hospital IT head, legal/compliance) and record names, time and case number.
2. Coordinate with clinical leads. Patient safety overrides forensic convenience; agree which systems must stay online.
3. Keep unauthorised people away from the affected area. Start the scene log.

## 2. Secure and document the scene

1. Photograph the scene before touching anything: screens, ransom messages, rack, cabling, device labels and serial numbers.
2. Record system clock vs real time, visible alerts, logged-in users and connected devices.
3. Draw a scene sketch and mark photograph points (see images/fig02_scene_sketch.png).
4. Note every device present: workstations, servers, USB media, mobile phones, network gear.

## 3. Contain without destroying evidence

1. Isolate the affected network segment (disable switch port or VLAN). Do not power devices off unless instructed.
2. Do not log in with additional accounts, run clean-up tools or delete files.
3. Disable or reset compromised accounts only after volatile data has been captured.

## 4. Capture volatile data (order of volatility)

1. RAM image, running processes, network connections, logged-in sessions.
2. Open files, scheduled tasks, services, clipboard.
3. Record commands used and who ran them, with timestamps.

## 5. Acquire persistent evidence

1. Use a hardware write blocker where possible.
2. Create a bit-stream image (FTK Imager or dd). Record source make, model, serial and capacity.
3. Calculate SHA-256 of source and image; they must match.
4. Work only on copies of the image; keep the original sealed.

## 6. Tag, bag and transport

1. Assign unique evidence IDs (E01, E02, ...), tag each item and photograph it with its tag.
2. Place media in anti-static bags, seal and sign across the seal.
3. Start a chain-of-custody form for every item (documentation/chain_of_custody.csv).

## 7. Hand over and report

1. Hand over to the evidence custodian with signatures from both parties.
2. Report to the competent authorities: CERT-In (within 6 hours under the 2022 Directions) and the local cyber police.
3. Preserve logs (firewall, DNS, proxy, EDR, mail, VPN, cloud audit) and stop automatic log rotation.
