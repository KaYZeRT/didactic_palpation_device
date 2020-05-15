int DELAY = 0;
int LOW_VALUE = 0;
int HIGH_VALUE = 0;
int ACQUIRING_DATA = 0;

int INDEX = 0;
int INTERVAL = 0;
unsigned long CURRENT_TIME = 0;
int COMMAND_SLAVE = 0;
int POSITION_SLAVE = 0;
float SPEED_SLAVE = 0;
int COMMAND_MASTER = 0;
int POSITION_MASTER = 0;
float SPEED_MASTER = 0;
float FORCE_SLAVE = 0;
unsigned long ELAPSED_TIME = 0;

String INDEX_STR;
String INTERVAL_STR;
String CURRENT_TIME_STR;
String COMMAND_SLAVE_STR;
String POSITION_SLAVE_STR;
String SPEED_SLAVE_STR;
String COMMAND_MASTER_STR;
String POSITION_MASTER_STR;
String SPEED_MASTER_STR;
String FORCE_SLAVE_STR;
String ELAPSED_TIME_STR;

unsigned long START_TIME = 0;
unsigned long PREVIOUS_MILLIS = 0;


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
  }

  INDEX = 0;
  ELAPSED_TIME = 0;

  while (ACQUIRING_DATA == 1)
  {
    if (INDEX == 0)
    {
      START_TIME = millis();
      PREVIOUS_MILLIS = START_TIME;
    }

    Serial.print('b');  //b: begin

    // INDEX
    INDEX_STR = String(INDEX);
    Serial.print(INDEX);
    Serial.print(';');

    // CURRENT TIME
    CURRENT_TIME = millis();
    CURRENT_TIME_STR = String(CURRENT_TIME);
    
    // INTERVAL
    INTERVAL = CURRENT_TIME - PREVIOUS_MILLIS;
    INTERVAL_STR = String(INTERVAL);
    Serial.print(INTERVAL);
    Serial.print(';');

    Serial.print(CURRENT_TIME);
    Serial.print(';');

    //SIMULATION COMMAND FOR SLAVE AND MASTER
    
    if (ELAPSED_TIME < 1000)
    {
      COMMAND_SLAVE = LOW_VALUE;
      COMMAND_MASTER = LOW_VALUE + 2;
      COMMAND_SLAVE_STR = String(COMMAND_SLAVE);
      COMMAND_MASTER_STR = String(COMMAND_MASTER);
    }
    else
    {
      COMMAND_SLAVE = HIGH_VALUE;
      COMMAND_MASTER = HIGH_VALUE + 2;
      COMMAND_SLAVE_STR = String(COMMAND_SLAVE);
      COMMAND_MASTER_STR = String(COMMAND_MASTER);
    }

    Serial.print(COMMAND_SLAVE);
    Serial.print(';');

    // POSITION_SLAVE
    POSITION_SLAVE = random(-5000, 0);
    POSITION_SLAVE_STR = String(POSITION_SLAVE);
    Serial.print(POSITION_SLAVE);
    Serial.print(';');

    // SPEED_SLAVE
    SPEED_SLAVE = random(-70, 0);
    SPEED_SLAVE = SPEED_SLAVE / 10; //DIVIDE TO CREATE FLOAT
    SPEED_SLAVE_STR = String(SPEED_SLAVE);
    Serial.print(SPEED_SLAVE);
    Serial.print(';');

    Serial.print(COMMAND_MASTER);
    Serial.print(';');

    // POSITION_MASTER
    POSITION_MASTER = random(-5000, 0);
    POSITION_MASTER_STR = String(POSITION_MASTER);
    Serial.print(POSITION_MASTER);
    Serial.print(';');

    // SPEED_MASTER
    SPEED_MASTER = random(-70, 0);
    SPEED_MASTER = SPEED_MASTER / 10; //DIVIDE TO CREATE FLOAT
    SPEED_MASTER_STR = String(SPEED_MASTER);
    Serial.print(SPEED_MASTER);
    Serial.print(';');

    // FORCE_SLAVE
    FORCE_SLAVE = random(1, 70);
    FORCE_SLAVE = FORCE_SLAVE / 100; //DIVIDE TO CREATE FLOAT
    FORCE_SLAVE_STR = String(FORCE_SLAVE);
    Serial.print(FORCE_SLAVE);
    Serial.print(';');

    

    // ELAPSED TIME SINCE FIRST MEASUREMENT
    //int elapsed_time = current_time - start_time;
    ELAPSED_TIME = CURRENT_TIME - START_TIME;
    ELAPSED_TIME_STR = String(ELAPSED_TIME);
    Serial.print(ELAPSED_TIME);
    Serial.println('e'); //e: end

    // SEND 

    //Serial.flush();
    //Serial.println(INDEX_STR + ";" + INTERVAL_STR + ";" + CURRENT_TIME_STR + ";" + COMMAND_SLAVE_STR + ";" + POSITION_SLAVE_STR + ";" + SPEED_SLAVE_STR + ";" + COMMAND_MASTER_STR + ";" + POSITION_MASTER_STR + ";" + SPEED_MASTER_STR + ";" + FORCE_SLAVE_STR + ";" + ELAPSED_TIME_STR);
    
    //float list_of_values[] = {(float) index, (float) interval, (float) current_time, (float) command_slave, (float) position_slave, speed_slave, (float) command_master, (float) position_master, speed_master, force_slave, (float) elapsed_time};
    
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
        }
      }
      Serial.read(); // CLEARS THE RECEIVING BUFFER - PREVENTS BUGS
    }

    INDEX++;
    PREVIOUS_MILLIS = CURRENT_TIME;
    delay(DELAY);
    Serial.flush();

  } // END OF WHILE(ACQUIRING_DATA==1)


} //END OF VOID LOOP()
