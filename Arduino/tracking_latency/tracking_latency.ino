short right_LED = 12;
short left_LED = 9;

bool led_state = 0;
int trial = 0;
int counter = 1;
int delay_count = 100;
int received_data = 0;

void setup() {
  
  // initialize digital LED pin as an output.
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(right_LED, OUTPUT);
  pinMode(left_LED, OUTPUT);
  
  // set the LEDs high or low
  digitalWrite(10, HIGH);
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

    if (received_data == 76){ // ord('L')
      digitalWrite(right_LED, LOW);
      digitalWrite(left_LED, HIGH);
    }

    if (received_data == 82){ // ord('R')
      digitalWrite(right_LED, HIGH);
      digitalWrite(left_LED, LOW);
    }
  }
}
