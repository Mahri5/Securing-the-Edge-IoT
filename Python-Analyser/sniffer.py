import logging
from datetime import datetime
from scapy.all import sniff, IP, TCP, Raw

# Setup logger for test execution traceability
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger("IoT_Analyzer")

PORT_MAP = {80: "HTTP", 1883: "MQTT"}

def packet_callback(pkt):
    """
    Packet filtering and payload extraction for cleartext vulnerability validation
    """
    if not pkt.haslayer(TCP) or not pkt.haslayer(Raw):
        return

    # Protocol mapping via set intersection (efficient port checking)
    dport, sport = pkt[TCP].dport, pkt[TCP].sport
    target_ports = set(PORT_MAP.keys())
    
    if target_ports.intersection({dport, sport}):
        proto = PORT_MAP.get(dport) or PORT_MAP.get(sport)
        
        # Raw payload extraction for empirical evidence
        try:
            payload = pkt[Raw].load.decode('utf-8', errors='ignore').strip()
            if payload:
                logger.info(f"VULNERABILITY EXPOSED [{proto}]: {pkt[IP].src} -> {pkt[IP].dst}")
                logger.info(f"Captured Payload: {payload}")
        except Exception:
            logger.warning("Payload decoding failed (likely binary/encrypted data)")

if __name__ == "__main__":
    logger.info("Initializing cleartext traffic monitor on standard IoT ports...")
    try:
        sniff(filter="tcp port 80 or tcp port 1883", prn=packet_callback, store=0)
    except KeyboardInterrupt:
        logger.info("Execution terminated by user.")