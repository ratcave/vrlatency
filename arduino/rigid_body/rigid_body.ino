short right_LED = 8;
short left_LED = 10;

void setup() {
  // initialize digital LED pin as an output.
  pinMode(9, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(right_LED, OUTPUT);
  
  // set the LEDs high or low
  digitalWrite(9, HIGH);
  digitalWrite(11, HIGH);
  digitalWrite(right_LED, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
}
