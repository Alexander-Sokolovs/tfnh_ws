String nom = "Arduino";
String msg;
void setup() {
 Serial.begin(1000000);
}
void loop() {
 readSerialPort();
 if (msg != "") {
   sendData();
 }else{
  Serial.println("hb");
 }
 delay(50);
}
void readSerialPort() {
 msg = "";
 if (Serial.available()) {
   delay(10);
   while (Serial.available() > 0) {
     msg += (char)Serial.read();
   }
   Serial.flush();
 }
}
void sendData() {
 //write data
 Serial.print(nom);
 Serial.print(" received : ");
 Serial.println(msg);
}
