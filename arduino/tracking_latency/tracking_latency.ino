short right_LED = 8;
short left_LED = 10;
int received_data = 0;
bool toggle = true;

void setup() {
  
  // initialize digital LED pin as an output.
  pinMode(9, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(right_LED, OUTPUT);
  pinMode(left_LED, OUTPUT);
  
  // set the LEDs high or low
  digitalWrite(9, HIGH);
  digitalWrite(11, HIGH);
  digitalWrite(right_LED, HIGH);
  digitalWrite(left_LED, LOW);

  // start seria comm
  Serial.begin(250000);       //  setup serial
  Serial.write("\n");         // 1 byte 
}

void loop() {
  if (Serial.available() > 0) {
    received_data = Serial.read();
    toggle = !toggle;
    if(toggle){
      digitalWrite(right_LED, LOW);
      digitalWrite(left_LED, HIGH);
      }
    else{
      digitalWrite(right_LED, HIGH);
      digitalWrite(left_LED, LOW);
      }
  }
}
