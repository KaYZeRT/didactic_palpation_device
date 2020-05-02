int acquisition_rate = 1000;

int line_number = 1;
int interval = 10000;
int time_s = 14083;

void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);
  
}

void loop() {
  // put your main code here, to run repeatedly:

  Serial.print(line_number);
  Serial.print("\t");
  Serial.print(interval);
  Serial.print("\t");
  Serial.print(time_s);
  Serial.print("\t");

  int command_slave = random(1, 4095);
  Serial.print(command_slave);
  Serial.print("\t");
  
  int position_slave = random(2, 1200);
  Serial.print(position_slave);
  Serial.print("\t");
  
  float speed_slave = random(1, 70); //divided to create float
  speed_slave = speed_slave/10;
  Serial.print(speed_slave);
  Serial.print("\t");

  int command_master = random(1, 4095);
  Serial.print(command_master);
  Serial.print("\t");
  
  int position_master = random(2, 1200);
  Serial.print(position_master);
  Serial.print("\t");
  
  float speed_master = random(1, 70); //divided to create float
  speed_master = speed_master/10;
  Serial.print(speed_master);
  Serial.print("\t");

  float force = random(1, 500);
  force = force/100;
  Serial.println(force);

  delay(acquisition_rate);

  line_number += 1;
  time_s += interval;

}
