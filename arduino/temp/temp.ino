int INTERVAL = 10;
int LOW_VALUE = 0;
int HIGH_VALUE = 0;
int ACQUIRING_DATA = 0;

int INDEX = 0;
//INTERVAL HERE (SEE GlobalConfig.COLUMNS)
int TIME = 0;
int COMMAND_SLAVE = 0;
int POSITION_SLAVE = 0;
float SPEED_SLAVE = 0;
int COMMAND_MASTER = 0;
int POSITION_MASTER = 0;
float SPEED_MASTER = 0;
float FORCE_SLAVE = 0;
int ELAPSED_TIME = 0;

void toggle_acquiring_data()
{
  if (ACQUIRING_DATA == 0)
  {
    ACQUIRING_DATA = 1;
  }
  else
  {
    ACQUIRING_DATA = 0;
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:

  //RECEIVING DATA FROM PYTHON
  String received_string = Serial.readString();
  Serial.print("Received Value: ");
  Serial.println(received_string);

  //GETTING FREQUENCY FROM STRING
  int index1 = received_string.indexOf('-');
  String interval_str = received_string.substring(0, index1);
  int INTERVAL = interval_str.toInt();
  Serial.print("INTERVAL: ");
  Serial.println(INTERVAL);

  //GETTING LOW_VALUE FROM STRING
  int index2 = received_string.indexOf('-', index1 + 1);
  String low_value_str = received_string.substring(index1 + 1, index2);
  int LOW_VALUE = low_value_str.toInt();
  Serial.print("LOW_VALUE: ");
  Serial.println(LOW_VALUE);

  //GETTING HIGH_VALUE FROM STRING
  int index3 = received_string.indexOf('-', index2 + 1);
  String high_value_str = received_string.substring(index2 + 1, index3);
  int HIGH_VALUE = high_value_str.toInt();
  Serial.print("HIGH_VALUE: ");
  Serial.println(HIGH_VALUE);

  //GETTING SENDING_DATA FROM STRING
  String sending_data_str = received_string.substring(index3 + 1);
  int toggle = sending_data_str.toInt();
  if (toggle == 1)
  {
    toggle_acquiring_data();
  }
  Serial.print("ACQUIRING_DATA: ");
  Serial.println(ACQUIRING_DATA);


  ACQUIRING_DATA = 1;
  while (ACQUIRING_DATA == 1)
  {
    TIME = millis();

    //SENDING RANDOM DATA

    //POSITION_SLAVE
    POSITION_SLAVE = random(-5000, 0);

    //SPEED_SLAVE
    SPEED_SLAVE = random(-70, 0);
    SPEED_SLAVE = SPEED_SLAVE / 10; //DIVIDE TO CREATE FLOAT

    //POSITION_MASTER
    POSITION_MASTER = random(-5000, 0);

    //SPEED_MASTER
    SPEED_MASTER = random(-70, 0);
    SPEED_MASTER = SPEED_MASTER / 10; //DIVIDE TO CREATE FLOAT

    //FORCE_SLAVE
    FORCE_SLAVE = random(1, 70);
    FORCE_SLAVE = FORCE_SLAVE / 100; //DIVIDE TO CREATE FLOAT

    String index = String(INDEX);
    String interval = String(INTERVAL);
    String time_str = String(TIME);
    String command_slave = String(COMMAND_SLAVE);
    String position_slave = String(POSITION_SLAVE);
    String speed_slave = String(SPEED_SLAVE);
    String command_master = String(COMMAND_MASTER);
    String position_master = String(POSITION_MASTER);
    String speed_master = String(SPEED_MASTER);
    String force_slave = String(FORCE_SLAVE);
    String elapsed_time = String(ELAPSED_TIME);

    //  Serial.println(INDEX);

    Serial.println(index + ";" + interval + ";" + time_str + ";" + command_slave + ";" + position_slave + ";" + speed_slave + ";" + command_master + ";" + position_master + ";" + speed_master + ";" + force_slave + ";" + elapsed_time);

    //CHECK WHETHER WE SHOULD STOP OR NOT
//    String received_string = Serial.readString();
//    int toggle = received_string.toInt();
//    if (toggle == 1)
//    {
//      toggle_acquiring_data();
//      Serial.print("ACQUIRING_DATA: ");
//      Serial.println(ACQUIRING_DATA);
//    }

    delay(INTERVAL);

    ELAPSED_TIME += INTERVAL;
    INDEX++;
  }

  INDEX = 0;
}
