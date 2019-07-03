void setup() {
  
  // put your setup code here, to run once:
  int volt = 5;
  
  serial.begin(9600);
  Ser = serial.Serial();
  baud   = 9600;
  
}

void loop() {
  // put your main code here, to run repeatedly:
  mes = Ser.read()

  if (mes == 1){

    
  }
}
