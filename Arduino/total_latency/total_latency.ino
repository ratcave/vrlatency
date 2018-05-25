short right_LED = 12;
short left_LED = 9;
int analogPin_Left = 2;         // Left PhotoDiode connect on anaglog pin2  
int analogPin_Right = 3;        // Right PhotoDiode connect on anaglog pin3  

bool led_state = 0;
int trial = 0;
int counter = 1;
int delay_count = 100;

struct Packet {
  unsigned long time_m;
  int left; 
  int right;
  int trial_no;
  bool LED_state;
};

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
  
  // switch LEDs and send timing data
  if (counter==delay_count){
    
    trial++;
    counter = 1;
    delay_count = random(100, 300); // this keeps the minimum interval at 100 - necessary for window!
    
    if (led_state){
      digitalWrite(right_LED, LOW);
      digitalWrite(left_LED, HIGH);
      led_state = 0;
      }
    else{
      digitalWrite(right_LED, HIGH);
      digitalWrite(left_LED, LOW);
      led_state = 1;
      }
  }
  
  Packet data = {micros(), analogRead(analogPin_Left)/50, analogRead(analogPin_Right)/50, trial, led_state};
  Serial.write((byte*)&data, 11);
  counter++;
}
