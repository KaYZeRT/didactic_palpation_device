int ACQUISITION_FREQUENCY = 0;
int LOW_VALUE = 0;
int HIGH_VALUE = 0;
int SENDING_DATA = 0;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

}

void loop() {
  // put your main code here, to run repeatedly:
  
  if (Serial.available())
  {
    //RECEIVING DATA FROM PYTHON
    String received_string = Serial.readString();
    Serial.print("Received Value: ");
    Serial.println(received_string);

    //GETTING FREQUENCY FROM STRING
    int index1 = received_string.indexOf('-');
    String frequency_str = received_string.substring(0, index1);
    int ACQUISITION_FREQUENCY = frequency_str.toInt();

    Serial.print("FREQUENCY: ");
    Serial.println(ACQUISITION_FREQUENCY);

    //GETTING LOW_VALUE FROM STRING
    int index2 = received_string.indexOf('-', index1+1);
    String low_value_str = received_string.substring(index1+1, index2);
    int LOW_VALUE = low_value_str.toInt();

    Serial.print("LOW_VALUE: ");
    Serial.println(LOW_VALUE);

    //GETTING HIGH_VALUE FROM STRING
    int index3 = received_string.indexOf('-', index2+1);
    String high_value_str = received_string.substring(index2+1, index3);
    int HIGH_VALUE = high_value_str.toInt();

    Serial.print("HIGH_VALUE: ");
    Serial.println(HIGH_VALUE);

    //GETTING SENDING_DATA FROM STRING
    String sending_data_str = received_string.substring(index3+1);
    int SENDING_DATA = sending_data_str.toInt();

    Serial.print("SENDING_DATA: ");
    Serial.println(SENDING_DATA);
    
  }

}
