int analogPin_Left = 2;         // Left PhotoDiode connect on anaglog pin2  
int analogPin_Right = 3;        // Right PhotoDiode connect on anaglog pin3  

bool start_recording = 0;
int received_data = 0;
int start_trial = 83;
int trial = 0;
int i = 0;

struct Packet {
  unsigned long time_m;
  int left; 
  int trial;
};

void setup() {

  // start serial comm
  Serial.begin(250000);       //  setup serial
  Serial.write("\n");         // 1 byte
  
}

void loop() {

  // ping test
  if (Serial.available() > 0) {
    received_data = Serial.read();

    if (received_data == start_trial){  // S
      trial += 1;
//      start_recording = 1;
      i = 0;
    }
  }

//  if (start_recording == 1){
    while (i < 240){
      Packet data = {micros(), analogRead(analogPin_Left)/50, trial};
      Serial.write((byte*)&data, 8);
      i++;
    }
//  }
}
