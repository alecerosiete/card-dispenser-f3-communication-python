import serial
import time

class CardDispenser:
    def __init__(self, port, baudrate=9600):
        self.ser = serial.Serial(port, baudrate)
    
    def send_command(self, command, parameter):
        packet = self._build_packet(command, parameter)
        self.ser.write(packet)
        time.sleep(0.1)
        #-- esta lectura es raw
        response = self.ser.read_all()
        
        if response:
            if response[0] == 0x06:  # Verificar si es un ACK (reconocimiento)
                print("Reconocimiento (ACK) recibido")
                print("Respuesta del dispositivo:", response.hex())
               
         
    def _build_packet(self, command, parameter):
       
        # Build packet for initialization device
        packet = bytearray()
        packet.append(0xF2)  # STX
        packet.append(0x00)  # ADDR
        packet.append(0x00)  # LENH
        packet.append(0x03)  # LENL
        packet.append(0x43)  # CMT
        packet.append(command)  # CM
        packet.append(parameter)  # PM and DATA
        packet.append(0x03)  # ETX
    
        
        # Calculate BCC
        bcc = self._calculate_bcc(packet)
        packet.append(bcc)
        
        return packet
    
    def _calculate_bcc(self, packet):
        bcc = 0
        for byte in packet:
            bcc ^= byte
        return bcc

# Ejemplo de uso para enviar el comando 33H
if __name__ == "__main__":
    dispenser = CardDispenser('COM3', baudrate=9600)
    dispenser.send_command(command=0x30, parameter=0x33)
    
