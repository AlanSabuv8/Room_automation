int LED_REG3 = 10;
int LED_REG4 = 11;
int LED_REG1 = 8;
int LED_REG2 = 9;

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    // Read the incoming data as a string
    String receivedData = Serial.readStringUntil('\n');

    // Parse the values from the string
    int values[4];  // Adjust the array size based on the number of values
    int count = 0;

    char *token = strtok(const_cast<char*>(receivedData.c_str()), ",");
    while (token != NULL) {
      values[count] = atoi(token);
      count++;
      token = strtok(NULL, ",");
    }

    // Process the values as needed
    if(values[0] == 1)
    {
      digitalWrite(LED_REG1,HIGH);
    }
    else
    {
      digitalWrite(LED_REG1,LOW);
    }
    if(values[1] == 1)
    {
      digitalWrite(LED_REG2,HIGH);
    }
    else
    {
      digitalWrite(LED_REG2,LOW);
    }
    if(values[2] == 1)
    {
      digitalWrite(LED_REG3,HIGH);
    }
    else
    {
      digitalWrite(LED_REG3,LOW);
    }
    if(values[3] == 1)
    {
      digitalWrite(LED_REG4,HIGH);
    }
    else
    {
      digitalWrite(LED_REG4,LOW);
    }
  }
}
