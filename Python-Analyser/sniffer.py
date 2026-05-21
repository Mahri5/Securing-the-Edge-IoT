from scapy.all import sniff, IP, TCP, Raw
import datetime

def analyze_packet(packet):
    # Check if the packet has IP and TCP layers
    if packet.haslayer(IP) and packet.haslayer(TCP):
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        dst_port = packet[TCP].dport
        src_port = packet[TCP].sport

        # We are only interested in unencrypted IoT traffic: HTTP (80) and unencrypted MQTT (1883)
        if dst_port in [80, 1883] or src_port in [80, 1883]:
            
            # Check if the packet contains a raw payload
            if packet.haslayer(Raw):
                payload = packet[Raw].load
                
                # Determine protocol for the thesis results table
                protocol = "HTTP" if (dst_port == 80 or src_port == 80) else "MQTT"
                
                current_time = datetime.datetime.now().strftime('%H:%M:%S')
                
                print(f"[{current_time}] ⚠️ ALERT: Unencrypted {protocol} packet intercepted!")
                print(f"Route: {src_ip} -> {dst_ip}")
                
                try:
                    # Attempt to decode the payload to read sensor data
                    decoded_data = payload.decode('utf-8', errors='ignore')
                    print(f"Intercepted Sensor Data: {decoded_data.strip()}")
                except Exception as e:
                    print(f"Raw Payload (undecodable): {payload}")
                
                print("-" * 60)

if __name__ == "__main__":
    print("=" * 60)
    print("🛡️ Starting IoT Traffic Analyzer (Securing the Edge)")
    print("📡 Listening on network for unencrypted protocols (HTTP/MQTT)...")
    print("Press Ctrl+C to stop the script.")
    print("=" * 60)
    
    # Start sniffing. store=0 prevents RAM overload.
    sniff(filter="tcp port 80 or tcp port 1883", prn=analyze_packet, store=0)
    