
import tkinter as tk
from tkinter import messagebox
import serial
import time
import threading


arduino_port = "COM5" 
baud_rate = 9600
arduino = None

# Función para conectar al Arduino y enviar el límite de temperatura
def conectar():
    global arduino
    try:
        arduino = serial.Serial(arduino_port, baud_rate)
        time.sleep(2) # Espera para que se establezca la conexion
        #modifica el lb para indicar conexion
        lbConection.config(text="Estado: Conectado", fg="green")
        messagebox.showinfo("Conexion", "Conexion establecida. ")
        start_reading() # lee los datos del arduino
    except serial.SerialException:
        messagebox.showerror("Error", "No se pudo conectar al Arduino. Verifique")
    except serial.SerialException as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar al Arduino: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")
        


# Función para desconectar el Arduino
def desconectar():
    global arduino
    if arduino and arduino.is_open:
        arduino.close() # ierra la conexion con el arduino
        #modifica el label para indicar desconexion
        lbConection.config(text="Estado: Desconectado", fg="red")
        messagebox.showinfo("Conexion", "Conexion terminada. ")
    else:
        messagebox.showwarning("Advertencia", "No hay conexion activa.")

# Funcion para enviar el limite de temperatura al Arduino
def enviar_limite():
    global arduino
    if arduino and arduino.is_open:
        try:
            limite = tbLimTemp.get()
            if limite.isdigit(): # Verifica si el límite es un número válido
                arduino.write(f"{limite}\n".encode()) # Envia el limite al Arduino
                messagebox.showinfo("Enviado", f"Limite de temperatura ({limite}C) enviado.")
            else:
                messagebox.showerror("Error", "Ingrese un valor numerico para el Limite. ")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el limite: {e}")
    else:
        messagebox.showwarning("Advertencia", "Conectese al Arduino antes de enviar el limite. ")

# Función para leer datos desde el Arduino
def read_from_arduino():
    global arduino
    while arduino and arduino.is_open:
        try:
            data = arduino.readline().decode().strip() # Lee los datos de temperatura
            if "Temperatura" in data: # Filtra solo las lineas que contienen temperatura
                temp_value = data.split(":")[1].strip().split(" ")[0]
                lbTemp.config(text=f"{temp_value} ℃")
            time.sleep(1)
        except Exception as e:
            print(f"Error leyendo datos: {e}")
            break

# Función para iniciar la lectura en un hilo separado
def start_reading():
    thread = threading. Thread(target=read_from_arduino)
    thread.daemon = True
    thread.start()

# Interfaz Grafica
root = tk.Tk()
root. title("Interfaz de Monitoreo de Temperatura")
root.geometry("300x350")

# lb título de temperatura
lbTitleTemp = tk.Label(root, text="Temperatura Actual", font=("Arial", 12))
lbTitleTemp.pack(pady=10)

# lb para mostrar la temperatura
lbTemp = tk.Label(root, text=" -- ℃", font=("Arial", 24))
lbTemp.pack()

# lb de estado de conexión
lbConection = tk.Label(root, text="Estado: Desconectado", fg="red", font=("Arial", 10))
lbConection.pack(pady=5)

# lb límite de temperatura
lbLimitTemp = tk.Label(root, text="Limite de Temperatura:")
lbLimitTemp.pack(pady=5)
tbLimTemp = tk.Entry(root, width=10)
tbLimTemp.pack(pady=5)

# Btn para enviar el límite de temperatura
btnEnviar = tk. Button(root, text="Enviar Limite", command=enviar_limite, font=("Arial", 10))
btnEnviar.pack(pady=5)

# Btn Conectar
btnConectar = tk.Button(root, text="Conectar", command=conectar, font=("Arial", 10))
btnConectar.pack(pady=5)

# Btn Desconectar
btnDesconectar = tk.Button(root, text="Desconectar", command=desconectar, font=("Arial", 10))
btnDesconectar.pack(pady=5)

root.mainloop()


"""
#include <Servo.h>
const int analogIn = A0;
const int servopin = 9; // Pin al que está conectado el motor
int temperatureLimit = 28; // Limite de temperatura inicial
int temperatureLimitSerial = -1; 

int RawValue = 0;
double Voltage = 0;
double tempC = 0;
double tempF = 0;
Servo Servo1;
void setup() {
  Serial.begin(9600);
  Servo1.attach(servopin);
}
void loop() {
  if (Serial.available() > 0) {
    temperatureLimitSerial = Serial.parseInt(); // Lee el limite de temperatura desde serial
    Serial.println("Valor recibido:");
    Serial.println(temperatureLimitSerial);
  }
  RawValue = analogRead(analogIn);//lee la temperatura
  Voltage = (RawValue / 1023.0) * 5000; // 5000 para obtener milivoltios
  tempC = Voltage * 0.1; // Celsius
  tempF = (tempC * 1.8) + 32; // Fahrenheit

  Serial.print("Temperatura (C): ");
  Serial.println(tempC, 1);
  // serial si fue recibido un nuevo limite lo usa, de lo contrario el local)
  int currentLimit = (temperatureLimitSerial != -1) ? temperatureLimitSerial : temperatureLimit;
  // Controla el motor en funcion del limite de temperatura
  if (tempC > currentLimit) {//mueve al servo
    Servo1.write(0);
    delay(1000);
    Servo1.write(90);
    delay(1000);
    Servo1.write(180);
    delay(1000);
  } else {
  Servo1.write(90); // Manten el servo en el centro (90 grados) como estado de reposo
  }
  delay(5000); // Espera antes de volver a leer la temperatura
}
"""