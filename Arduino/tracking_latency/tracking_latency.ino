// Left LEDs: 11, 12, 13
// Right LEDs: 8, 9, 10

short right_LEDs[] = {8, 9, 10}; 
short left_LEDs[] = {11, 12, 13};  

bool led_state = 0;
int trial = 0;
int counter = 1;
int delay_count = 100;
int received_data = 0;

void setup() {
  
  // initialize digital LED pin as an output.
  for (int i=0; i<sizeof(right_LEDs); i++){
    pinMode(right_LEDs[i], OUTPUT);
    pinMode(left_LEDs[i], OUTPUT);
    }

  // set the LEDs high or low
  set_LEDs(left_LEDs, 3, HIGH);
  set_LEDs(right_LEDs, 3, LOW);

  // start seria comm
  Serial.begin(250000);       //  setup serial
  Serial.write("\n");         // 1 byte
  
}

void set_LEDs(short *array_of_LEDs, short array_size, bool level){
  for (int i=0; i<array_size; i++){
    digitalWrite(array_of_LEDs[i], level);
    }
  }

void loop() {
  if (Serial.available() > 0) {
    received_data = Serial.read();

    if (received_data == 76){ // ord('L')
      set_LEDs(left_LEDs, 3, HIGH);
      set_LEDs(right_LEDs, 3, LOW);
    }

    if (received_data == 82){ // ord('R')
      set_LEDs(left_LEDs, 3, LOW);
      set_LEDs(right_LEDs, 3, HIGH);
    }
  }
}
