int DELAY = 0;
int LOW_VALUE = 0;
int HIGH_VALUE = 0;
int ACQUIRING_DATA = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0)
  {
    if (Serial.peek() == 'c' && ACQUIRING_DATA == 0)
    {
      Serial.read();

      //RECEIVING DATA FROM PYTHON
      String received_string = Serial.readString();
      //      Serial.print("Received Value: ");
      //      Serial.println(received_string);

      //GETTING FREQUENCY FROM STRING
      int index1 = received_string.indexOf('-');
      String delay_str = received_string.substring(0, index1);
      DELAY = delay_str.toInt();
      //      Serial.print("DELAY: ");
      //      Serial.println(DELAY);

      //GETTING LOW_VALUE FROM STRING
      int index2 = received_string.indexOf('-', index1 + 1);
      String low_value_str = received_string.substring(index1 + 1, index2);
      LOW_VALUE = low_value_str.toInt();
      //      Serial.print("LOW_VALUE: ");
      //      Serial.println(LOW_VALUE);

      //GETTING HIGH_VALUE FROM STRING
      int index3 = received_string.indexOf('-', index2 + 1);
      String high_value_str = received_string.substring(index2 + 1, index3);
      HIGH_VALUE = high_value_str.toInt();
      //      Serial.print("HIGH_VALUE: ");
      //      Serial.println(HIGH_VALUE);

      //GETTING TOGGLE FROM STRING
      String acquiring_data_str = received_string.substring(index3 + 1);
      int temp = acquiring_data_str.toInt();
      if (temp == 1)
      {
        ACQUIRING_DATA = temp;
      }
      //      Serial.print("ACQUIRING_DATA: ");
      //      Serial.println(ACQUIRING_DATA);
    }
    Serial.read(); // CLEARS THE RECEIVING BUFFER - PREVENTS BUGS
//    Serial.flush(); // CLEARS THE TRRANSMITTING BUFFER - PREVENTS BUGS
  }

  int index = 0;
  int start_time = 0;
  int previous_millis = 0;
  String command_slave_str;
  String command_master_str;

  while (ACQUIRING_DATA == 1)
  {
    if (index == 0)
    {
      start_time = millis();
      previous_millis = start_time;
    }

    // INDEX
    String index_str = String(index);

    // POSITION_SLAVE
    int position_slave = random(-5000, 0);
    String position_slave_str = String(position_slave);

    // SPEED_SLAVE
    float speed_slave = random(-70, 0);
    speed_slave = speed_slave / 10; //DIVIDE TO CREATE FLOAT
    String speed_slave_str = String(speed_slave);

    // POSITION_MASTER
    int position_master = random(-5000, 0);
    String position_master_str = String(position_master);

    // SPEED_MASTER
    float speed_master = random(-70, 0);
    speed_master = speed_master / 10; //DIVIDE TO CREATE FLOAT
    String speed_master_str = String(speed_master);

    // FORCE_SLAVE
    float force_slave = random(1, 70);
    force_slave = force_slave / 100; //DIVIDE TO CREATE FLOAT
    String force_slave_str = String(force_slave);

    // CURRENT TIME
    int current_time = millis();
    String current_time_str = String(current_time);

    // ELAPSED TIME SINCE FIRST MEASUREMENT
    int elapsed_time = current_time - start_time;
    String elapsed_time_str = String(elapsed_time);

    // INTERVAL
    int interval = current_time - previous_millis;
    String interval_str = String(interval);

    //SIMULATION COMMAND FOR SLAVE AND MASTER
    if (current_time < 1000)
    {
      int command_slave = LOW_VALUE;
      int command_mater = LOW_VALUE + 2;
      command_slave_str = String(command_slave);
      command_master_str = String(command_mater);
    }
    else
    {
      int command_slave = HIGH_VALUE;
      int command_mater = HIGH_VALUE + 2;
      command_slave_str = String(command_slave);
      command_master_str = String(command_mater);
    }

    // SEND DATA
    Serial.println(index_str + ";" + interval_str + ";" + current_time_str + ";" + command_slave_str + ";" + position_slave_str + ";" + speed_slave_str + ";" + command_master_str + ";" + position_master_str + ";" + speed_master_str + ";" + force_slave_str + ";" + elapsed_time_str);
    Serial.flush();

    //CHECK WHETHER WE SHOULD STOP OR NOT
    if (Serial.available() > 0)
    {
      if (Serial.peek() == 'c' && ACQUIRING_DATA == 1)
      {
        Serial.read();
        int temp = Serial.parseInt();
        if (temp == 0)
        {
          ACQUIRING_DATA = temp;
//          Serial.print("ACQUIRING_DATA: ");
//          Serial.println(ACQUIRING_DATA);
//          Serial.flush();
        }
      }
      Serial.read(); // CLEARS THE RECEIVING BUFFER - PREVENTS BUGS
    }

    index++;
    previous_millis = current_time;
    delay(DELAY);

  } // END OF WHILE(ACQUIRING_DATA==1)
//  Serial.flush(); // CLEARS THE TRRANSMITTING BUFFER - PREVENTS BUGS

} //END OF VOID LOOP()
